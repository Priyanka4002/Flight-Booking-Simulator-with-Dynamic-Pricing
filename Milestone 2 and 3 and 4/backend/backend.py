# backend.py
from fastapi import FastAPI, HTTPException, Depends, status, Query
from datetime import datetime
import asyncio, random
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware

from db_config import get_db, engine
from models import Airline, Reservation, Booking, FareHistory
from pricing_engine import calculate_dynamic_price
from utils import generate_pnr, flight_duration_minutes

from sqlalchemy.orm import Session
from sqlalchemy import func, select

from fastapi.responses import StreamingResponse
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

app = FastAPI(title="Airline Modular Backend (full features)")

# Allow frontend (localhost:5500) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Airline modular backend running"}

@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(select([func.now()]))
        return {"status": "ok", "db_connected": True}
    except Exception:
        return {"status": "ok", "db_connected": False}

@app.get("/flights")
def get_all_flights(db: Session = Depends(get_db)):
    return db.query(Airline).all()

@app.get("/search")
def search_flights(origin_city: str, destination_city: str,
                   departure_time: Optional[str] = None,
                   sort_by: Optional[str] = Query(None, regex="^(price|duration)$"),
                   db: Session = Depends(get_db)):
    query = db.query(Airline).filter(Airline.origin_city == origin_city,
                                     Airline.destination_city == destination_city)
    if departure_time:
        try:
            dt = datetime.strptime(departure_time, "%Y-%m-%d")
            query = query.filter(func.date(Airline.departure_time) == dt.date())
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid departure_time format. Use YYYY-MM-DD")
    flights = query.all()
    if not flights:
        raise HTTPException(status_code=404, detail="No matching flights found")
    results = []
    for f in flights:
        base = float(f.ticket_price) if f.ticket_price is not None else 0.0
        dyn = calculate_dynamic_price(base, f.available_seats or 0, f.capacity or 1, f.departure_time)
        results.append({
            "airline_code": f.airline_code,
            "operator_name": f.operator_name,
            "origin_city": f.origin_city,
            "destination_city": f.destination_city,
            "departure_time": f.departure_time.strftime("%Y-%m-%d %H:%M:%S") if f.departure_time else None,
            "arrival_time": f.arrival_time.strftime("%Y-%m-%d %H:%M:%S") if f.arrival_time else None,
            "available_seats": f.available_seats,
            "ticket_price": base,
            "dynamic_price": dyn,
            "duration_minutes": flight_duration_minutes(f.departure_time, f.arrival_time)
        })
    if sort_by == "price":
        results.sort(key=lambda x: x["dynamic_price"])
    elif sort_by == "duration":
        results.sort(key=lambda x: x["duration_minutes"])
    return results

@app.get("/dynamic_price/{airline_code}")
def dynamic_price(airline_code: str, db: Session = Depends(get_db)):
    flight = db.query(Airline).filter(Airline.airline_code == airline_code).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    old_price = float(flight.ticket_price or 0.0)
    new_price = calculate_dynamic_price(old_price, flight.available_seats, flight.capacity, flight.departure_time)
    db.add(FareHistory(flight_id=flight.airline_id, old_price=old_price, new_price=new_price))
    db.commit()
    return {"airline_code": airline_code, "dynamic_price": new_price, "base_price": old_price}

@app.get("/external_api/{provider}/flights/{airline_code}")
def external_schedule_mock(provider: str, airline_code: str, db: Session = Depends(get_db)):
    flight = db.query(Airline).filter(Airline.airline_code == airline_code).first()
    if not flight:
        return {"provider": provider, "airline_code": airline_code, "status": "not_found"}
    dep = flight.departure_time
    arr = flight.arrival_time
    return {
        "provider": provider,
        "airline_code": airline_code,
        "origin": flight.origin_city,
        "destination": flight.destination_city,
        "departure_time": dep.strftime("%Y-%m-%d %H:%M:%S") if dep else None,
        "arrival_time": arr.strftime("%Y-%m-%d %H:%M:%S") if arr else None,
        "base_fare": float(flight.ticket_price) if flight.ticket_price is not None else None,
        "seats_left": flight.available_seats
    }

# Legacy reservation model compatibility
from pydantic import BaseModel
from typing import Optional

class BookingRequest(BaseModel):
    airline_code: str
    passenger_name: str
    contact_number: str
    seat_number: Optional[int] = None

class BookingResponse(BaseModel):
    reservation_id: Optional[int]
    pnr: Optional[str]
    booking_id: Optional[int]
    airline_code: Optional[str]
    airline_id: Optional[int]
    passenger_name: str
    seat_number: int
    status: str
    price: Optional[float] = None

@app.post("/book", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(request: BookingRequest, db: Session = Depends(get_db)):
    flight = db.query(Airline).filter(Airline.airline_code == request.airline_code).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    if flight.available_seats is None or flight.available_seats <= 0:
        raise HTTPException(status_code=400, detail="No seats available")
    seat_no = request.seat_number if request.seat_number else random.randint(1, flight.capacity)
    flight.available_seats = max(0, flight.available_seats - 1)
    booking = Reservation(
        transaction_id=f"TXN{random.randint(1000,9999)}",
        airline_code=flight.airline_code,
        origin_city=flight.origin_city,
        destination_city=flight.destination_city,
        passenger_name=request.passenger_name,
        contact_number=request.contact_number,
        seat_number=seat_no
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return BookingResponse(
        reservation_id=booking.reservation_id,
        pnr=None,
        booking_id=None,
        airline_code=booking.airline_code,
        airline_id=None,
        passenger_name=booking.passenger_name,
        seat_number=booking.seat_number,
        status="Confirmed",
        price=None
    )

class BookingCreateRequest(BaseModel):
    airline_code: str
    passenger_name: str
    contact_number: Optional[str] = None
    seat_number: Optional[int] = None

@app.post("/bookings/create", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking_workflow(request: BookingCreateRequest, db: Session = Depends(get_db)):
    try:
        airline = db.query(Airline).filter(Airline.airline_code == request.airline_code).with_for_update().first()
        if not airline:
            raise HTTPException(status_code=404, detail="Flight not found")
        if airline.available_seats is None or airline.available_seats <= 0:
            raise HTTPException(status_code=400, detail="No seats available")
        seat_no = None
        if request.seat_number:
            existing = db.query(Booking).filter(
                Booking.airline_id == airline.airline_id,
                Booking.seat_number == request.seat_number,
                Booking.status.in_(["CONFIRMED", "PAID", "PENDING"])
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="Requested seat already taken")
            seat_no = request.seat_number
        else:
            taken_rows = db.query(Booking.seat_number).filter(Booking.airline_id == airline.airline_id).all()
            taken = {r[0] for r in taken_rows if r and r[0] is not None}
            for c in range(1, (airline.capacity or 1) + 1):
                if c not in taken:
                    seat_no = c
                    break
            if seat_no is None:
                raise HTTPException(status_code=500, detail="No seat assignable")
        price = calculate_dynamic_price(
            base_fare=float(airline.ticket_price or 0.0),
            seats_available=max(0, airline.available_seats - 1),
            capacity=airline.capacity,
            departure_time=airline.departure_time
        )
        attempts = 0
        pnr = generate_pnr()
        while db.query(Booking).filter(Booking.pnr == pnr).first():
            pnr = generate_pnr()
            attempts += 1
            if attempts > 10:
                raise HTTPException(status_code=500, detail="Unable to generate unique PNR")
        new_booking = Booking(
            pnr=pnr,
            airline_id=airline.airline_id,
            passenger_name=request.passenger_name,
            contact_number=request.contact_number,
            seat_number=seat_no,
            price=price,
            status="PENDING"
        )
        airline.available_seats = max(0, airline.available_seats - 1)
        db.add(new_booking)
        db.flush()
        db.commit()
        db.refresh(new_booking)
        return BookingResponse(
            reservation_id=None,
            pnr=new_booking.pnr,
            booking_id=new_booking.booking_id,
            airline_code=airline.airline_code,
            airline_id=airline.airline_id,
            passenger_name=new_booking.passenger_name,
            seat_number=new_booking.seat_number,
            status=new_booking.status,
            price=float(new_booking.price) if new_booking.price is not None else None
        )
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Booking failed: {e}")

@app.post("/bookings/{pnr}/pay")
def pay_booking(pnr: str, db: Session = Depends(get_db)):
    try:
        booking = db.query(Booking).filter(Booking.pnr == pnr).with_for_update().first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        if booking.status == "PAID":
            return {"pnr": pnr, "success": True, "status": "PAID", "message": "Already paid"}
        success = random.choice([True, True, False])
        if success:
            booking.status = "PAID"
            db.commit()
            return {"pnr": pnr, "success": True, "status": booking.status, "message": "Payment successful"}
        else:
            booking.status = "FAILED"
            airline = db.query(Airline).filter(Airline.airline_id == booking.airline_id).with_for_update().first()
            if airline:
                airline.available_seats = min(airline.capacity, (airline.available_seats or 0) + 1)
            db.commit()
            return {"pnr": pnr, "success": False, "status": booking.status, "message": "Payment failed"}
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Payment processing error: {e}")

@app.post("/bookings/{pnr}/confirm")
def confirm_booking(pnr: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.pnr == pnr).with_for_update().first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.status in ["CANCELLED"]:
        raise HTTPException(status_code=400, detail=f"Cannot confirm booking in status {booking.status}")
    if booking.status == "PAID":
        return {"pnr": pnr, "status": booking.status, "message": "Already paid/confirmed"}
    booking.status = "CONFIRMED"
    db.commit()
    return {"pnr": pnr, "status": booking.status}

@app.post("/bookings/{pnr}/cancel")
def cancel_booking(pnr: str, db: Session = Depends(get_db)):
    try:
        booking = db.query(Booking).filter(Booking.pnr == pnr).with_for_update().first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        if booking.status == "CANCELLED":
            return {"pnr": pnr, "status": booking.status, "message": "Already cancelled"}
        booking.status = "CANCELLED"
        airline = db.query(Airline).filter(Airline.airline_id == booking.airline_id).with_for_update().first()
        if airline:
            airline.available_seats = min(airline.capacity, (airline.available_seats or 0) + 1)
        db.commit()
        return {"pnr": pnr, "status": booking.status, "message": "Booking cancelled and seat restored"}
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Cancellation failed: {e}")

@app.get("/bookings/{pnr}")
def get_booking_by_pnr(pnr: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.pnr == pnr).first()
    if booking:
        return {
            "pnr": booking.pnr,
            "booking_id": booking.booking_id,
            "airline_id": booking.airline_id,
            "passenger_name": booking.passenger_name,
            "seat_number": booking.seat_number,
            "price": float(booking.price) if booking.price is not None else None,
            "status": booking.status,
            "created_at": booking.created_at.strftime("%Y-%m-%d %H:%M:%S") if booking.created_at else None
        }
    if pnr.isdigit():
        res = db.query(Reservation).filter(Reservation.reservation_id == int(pnr)).first()
        if res:
            return {
                "reservation_id": res.reservation_id,
                "transaction_id": res.transaction_id,
                "airline_code": res.airline_code,
                "passenger_name": res.passenger_name,
                "seat_number": res.seat_number,
            }
    raise HTTPException(status_code=404, detail="Booking not found")

@app.get("/bookings")
def list_or_filter_bookings(pnr: Optional[str] = None, booking_id: Optional[int] = None,
                           passenger_name: Optional[str] = None, airline_code: Optional[str] = None,
                           db: Session = Depends(get_db)):
    query = db.query(Booking)
    if booking_id:
        query = query.filter(Booking.booking_id == booking_id)
    if pnr:
        query = query.filter(Booking.pnr == pnr)
    if passenger_name:
        query = query.filter(Booking.passenger_name.ilike(f"%{passenger_name}%"))
    if airline_code:
        query = query.join(Airline).filter(Airline.airline_code == airline_code)
    results = query.all()
    return [{
        "pnr": b.pnr,
        "booking_id": b.booking_id,
        "airline_id": b.airline_id,
        "passenger_name": b.passenger_name,
        "seat_number": b.seat_number,
        "price": float(b.price) if b.price is not None else None,
        "status": b.status,
        "created_at": b.created_at.strftime("%Y-%m-%d %H:%M:%S") if b.created_at else None
    } for b in results]

@app.delete("/cancel/{reservation_id}")
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    booking = db.query(Reservation).filter(Reservation.reservation_id == reservation_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    flight = db.query(Airline).filter(Airline.airline_code == booking.airline_code).first()
    if flight:
        flight.available_seats = min(flight.capacity, (flight.available_seats or 0) + 1)
    db.delete(booking)
    db.commit()
    return {"message": f"Booking {reservation_id} cancelled successfully"}

@app.get("/bookings/legacy")
def get_all_legacy_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).all()

@app.get("/bookings/filter")
def filter_bookings(reservation_id: Optional[int] = None, airline_code: Optional[str] = None,
                   origin_city: Optional[str] = None, destination_city: Optional[str] = None,
                   passenger_name: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Reservation)
    if reservation_id:
        query = query.filter(Reservation.reservation_id == reservation_id)
    if airline_code:
        query = query.filter(Reservation.airline_code == airline_code)
    if origin_city:
        query = query.filter(Reservation.origin_city == origin_city)
    if destination_city:
        query = query.filter(Reservation.destination_city == destination_city)
    if passenger_name:
        query = query.filter(Reservation.passenger_name.ilike(f"%{passenger_name}%"))
    results = query.all()
    if not results:
        raise HTTPException(status_code=404, detail="No matching bookings found")
    return [{
        "reservation_id": b.reservation_id,
        "transaction_id": b.transaction_id,
        "airline_code": b.airline_code,
        "origin_city": b.origin_city,
        "destination_city": b.destination_city,
        "passenger_name": b.passenger_name,
        "contact_number": b.contact_number,
        "seat_number": b.seat_number
    } for b in results]

@app.get("/bookings/{pnr}/receipt")
def download_receipt(pnr: str, db: Session = Depends(get_db)):
    """Generate and return a booking receipt PDF for a given PNR or legacy reservation."""
    # Try modern booking first
    booking = db.query(Booking).filter(Booking.pnr == pnr).first()
    if not booking and pnr.isdigit():
        booking = db.query(Reservation).filter(Reservation.reservation_id == int(pnr)).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 800, "Airline Booking Receipt")
    pdf.setFont("Helvetica", 12)

    y = 770
    pdf.drawString(100, y, f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 20

    # Handle modern Booking table
    if hasattr(booking, "pnr"):
        airline = db.query(Airline).filter(Airline.airline_id == booking.airline_id).first()
        pdf.drawString(100, y, f"PNR: {booking.pnr}"); y -= 20
        pdf.drawString(100, y, f"Passenger: {booking.passenger_name}"); y -= 20
        pdf.drawString(100, y, f"Seat Number: {booking.seat_number}"); y -= 20
        pdf.drawString(100, y, f"Status: {booking.status}"); y -= 20
        pdf.drawString(100, y, f"Price: ₹{float(booking.price) if booking.price else 0.0}"); y -= 20
        if airline:
            pdf.drawString(100, y, f"Airline Code: {airline.airline_code}"); y -= 20
            pdf.drawString(100, y, f"Route: {airline.origin_city} → {airline.destination_city}"); y -= 20
            pdf.drawString(100, y, f"Departure: {airline.departure_time.strftime('%Y-%m-%d %H:%M:%S')}"); y -= 20
            pdf.drawString(100, y, f"Arrival: {airline.arrival_time.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        # Legacy Reservation
        pdf.drawString(100, y, f"Reservation ID: {booking.reservation_id}"); y -= 20
        pdf.drawString(100, y, f"Transaction ID: {booking.transaction_id}"); y -= 20
        pdf.drawString(100, y, f"Passenger: {booking.passenger_name}"); y -= 20
        pdf.drawString(100, y, f"Airline Code: {booking.airline_code}"); y -= 20
        pdf.drawString(100, y, f"Seat Number: {booking.seat_number}")

    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(100, 100, "Thank you for booking with our Airline Simulator!")
    pdf.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=receipt_{pnr}.pdf"
        },
    )

# Background market simulator
def simulate_market_step_once():
    db = next(get_db())
    flights = db.query(Airline).all()
    for f in flights:
        change = random.choice([-2, -1, 0, 0, 1])
        new_avail = max(0, min(f.capacity or 0, (f.available_seats or 0) + change))
        if new_avail != (f.available_seats or 0):
            old_price = float(f.ticket_price or 0.0)
            f.available_seats = new_avail
            new_price = calculate_dynamic_price(old_price, f.available_seats, f.capacity or 1, f.departure_time)
            db.add(FareHistory(flight_id=f.airline_id, old_price=old_price, new_price=new_price, changed_at=datetime.utcnow()))
    db.commit()
    db.close()

async def market_scheduler(interval_seconds: int = 300):
    while True:
        await asyncio.to_thread(simulate_market_step_once)
        await asyncio.sleep(interval_seconds)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(market_scheduler(interval_seconds=300))