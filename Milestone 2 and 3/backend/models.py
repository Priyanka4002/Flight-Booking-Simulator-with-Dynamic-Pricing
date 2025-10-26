# models.py
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime
from db_config import Base

class Airline(Base):
    __tablename__ = "airlines"
    airline_id = Column(Integer, primary_key=True, autoincrement=True)
    airline_code = Column(String(10))
    origin_city = Column(String(50))
    destination_city = Column(String(50))
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    ticket_price = Column(DECIMAL(10, 2))
    capacity = Column(Integer)
    available_seats = Column(Integer)
    operator_name = Column(String(20))
    reservations = relationship("Reservation", back_populates="airline")
    bookings = relationship("Booking", back_populates="airline")

class Reservation(Base):
    __tablename__ = "reservations"
    reservation_id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String(20))
    airline_code = Column(String(10), ForeignKey("airlines.airline_code"))
    origin_city = Column(String(50))
    destination_city = Column(String(50))
    passenger_name = Column(String(50))
    contact_number = Column(String(15))
    seat_number = Column(Integer)
    airline = relationship("Airline", back_populates="reservations")

class FareHistory(Base):
    __tablename__ = "fare_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer)
    old_price = Column(DECIMAL(10, 2))
    new_price = Column(DECIMAL(10, 2))
    changed_at = Column(DateTime, default=datetime.utcnow)

class Booking(Base):
    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    pnr = Column(String(20), unique=True, nullable=False)
    airline_id = Column(Integer, ForeignKey("airlines.airline_id"), nullable=False)
    passenger_name = Column(String(100), nullable=False)
    contact_number = Column(String(30))
    seat_number = Column(Integer)
    price = Column(DECIMAL(10, 2))
    status = Column(String(20), nullable=False)  # PENDING, CONFIRMED, PAID, CANCELLED, FAILED
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    airline = relationship("Airline", back_populates="bookings")