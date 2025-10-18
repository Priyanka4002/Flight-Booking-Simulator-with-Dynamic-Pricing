from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel

from .db_config import get_db
from .models import Airline, Reservation, FareHistory
from .pricing_engine import calculate_dynamic_price

import random


# Inline Pydantic Schemas (no need for separate schemas.py)

class BookingRequest(BaseModel):
    airline_code: str
    passenger_name: str
    contact_number: str
    seat_number: Optional[int] = None


class BookingResponse(BaseModel):
    reservation_id: int
    airline_code: str
    passenger_name: str
    seat_number: int
    status: str


class DynamicPriceResponse(BaseModel):
    airline_code: str
    origin_city: str
    destination_city: str
    base_price: float
    dynamic_price: float
    seats_left: int
    departure_time: str



# Initialize FastAPI App

app = FastAPI(title="Airline Dynamic Pricing & Booking API")



# Root Endpoint

@app.get("/")
def home():
    return {"message": "Airline Dynamic Pricing & Booking API is running"}



# Get All Flights

@app.get("/flights")
def get_all_flights(db: Session = Depends(get_db)):
    return db.query(Airline).all()



# Get Dynamic Price for a Flight
@app.get("/dynamic_price/{airline_code}", response_model=DynamicPriceResponse)
def get_dynamic_price(airline_code: str, db: Session = Depends(get_db)):
    flight = db.query(Airline).filter(Airline.airline_code == airline_code).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    old_price = float(flight.ticket_price)
    new_price = calculate_dynamic_price(
        base_fare=old_price,
        seats_available=flight.available_seats,
        capacity=flight.capacity,
        departure_time=flight.departure_time
    )

    db.add(FareHistory(
        flight_id=flight.airline_id,
        old_price=old_price,
        new_price=new_price,
        changed_at=datetime.utcnow()
    ))
    db.commit()

    return {
        "airline_code": flight.airline_code,
        "origin_city": flight.origin_city,
        "destination_city": flight.destination_city,
        "base_price": old_price,
        "dynamic_price": new_price,
        "seats_left": flight.available_seats,
        "departure_time": flight.departure_time.strftime("%Y-%m-%d %H:%M:%S")
    }



# Search Flights (GET Endpoint)

# 🔹 Search flights by origin, destination, and optional date/time
@app.get("/search")
def search_flights(
    origin_city: str,
    destination_city: str,
    departure_time: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Airline).filter(
        Airline.origin_city == origin_city,
        Airline.destination_city == destination_city
    )

    # If user passes a departure time filter
    if departure_time:
        try:
            dt = datetime.strptime(departure_time, "%Y-%m-%d %H:%M:%S")
            query = query.filter(Airline.departure_time == dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid departure_time format. Use YYYY-MM-DD HH:MM:SS")

    flights = query.all()
    if not flights:
        raise HTTPException(status_code=404, detail="No matching flights found")

    return [
        {
            "airline_code": f.airline_code,
            "operator_name": f.operator_name,
            "origin_city": f.origin_city,
            "destination_city": f.destination_city,
            "departure_time": f.departure_time.strftime("%Y-%m-%d %H:%M:%S"),
            "arrival_time": f.arrival_time.strftime("%Y-%m-%d %H:%M:%S"),
            "available_seats": f.available_seats,
            "ticket_price": float(f.ticket_price),
        }
        for f in flights
    ]



# Optional: Booking Endpoint (if you want booking feature)

@app.post("/book", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(request: BookingRequest, db: Session = Depends(get_db)):
    flight = db.query(Airline).filter(Airline.airline_code == request.airline_code).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    if flight.available_seats <= 0:
        raise HTTPException(status_code=400, detail="No seats available")

    seat_no = request.seat_number if request.seat_number else random.randint(1, flight.capacity)
    flight.available_seats -= 1

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

    return {
        "reservation_id": booking.reservation_id,
        "airline_code": booking.airline_code,
        "passenger_name": booking.passenger_name,
        "seat_number": booking.seat_number,
        "status": "Confirmed"
    }


@app.get("/bookings")
def get_all_bookings(db: Session = Depends(get_db)):
    return db.query(Reservation).all()

# Filter bookings by any combination of parameters
@app.get("/bookings/filter")
def filter_bookings(
    reservation_id: Optional[int] = None,
    airline_code: Optional[str] = None,
    origin_city: Optional[str] = None,
    destination_city: Optional[str] = None,
    passenger_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
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
        query = query.filter(Reservation.passenger_name.like(f"%{passenger_name}%"))

    results = query.all()

    if not results:
        raise HTTPException(status_code=404, detail="No matching bookings found")

    return [
        {
            "reservation_id": b.reservation_id,
            "transaction_id": b.transaction_id,
            "airline_code": b.airline_code,
            "origin_city": b.origin_city,
            "destination_city": b.destination_city,
            "passenger_name": b.passenger_name,
            "contact_number": b.contact_number,
            "seat_number": b.seat_number
        }
        for b in results
    ]