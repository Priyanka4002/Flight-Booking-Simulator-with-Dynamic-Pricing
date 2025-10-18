from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db_config import Base
from datetime import datetime

class Airline(Base):
    __tablename__ = "airlines"
    airline_id = Column(Integer, primary_key=True, autoincrement=True)
    airline_code = Column(String(10), unique=True, index=True)
    origin_city = Column(String(50))
    destination_city = Column(String(50))
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    ticket_price = Column(DECIMAL(10, 2))
    capacity = Column(Integer)
    available_seats = Column(Integer)
    operator_name = Column(String(20))
    reservations = relationship("Reservation", back_populates="airline")

class Reservation(Base):
    __tablename__ = "reservations"
    reservation_id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String(20), unique=True)
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
