from sqlalchemy import  Column, Integer, Float, Date, String, Text, ForeignKey, Enum, DECIMAL, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
import enum
from models.database import Base

# Models


class BookingStatusEnum(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    location = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    events = relationship('Event', back_populates='venue', cascade="all, delete-orphan")

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    venue_id = Column(Integer, ForeignKey('venues.id', ondelete='CASCADE'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    venue = relationship('Venue', back_populates='events')
    bookings = relationship('Booking', back_populates='event', cascade="all, delete-orphan")


class TicketType(Base):
    __tablename__ = 'ticket_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    bookings = relationship('Booking', back_populates='ticket_type', cascade="all, delete-orphan")


class Booking(Base):
    __tablename__ = 'bookings'
    __table_args__ = (
        UniqueConstraint('confirmation_code', name='uq_booking_confirmation_code'),
    )

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    venue_id = Column(Integer, ForeignKey('venues.id', ondelete='CASCADE'), nullable=False)
    ticket_type_id = Column(Integer, ForeignKey('ticket_types.id', ondelete='CASCADE'), nullable=False)

    quantity = Column(Integer, nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum(BookingStatusEnum), default=BookingStatusEnum.pending, nullable=False)
    confirmation_code = Column(String(20), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    event = relationship('Event', back_populates='bookings')
    ticket_type = relationship('TicketType', back_populates='bookings')
    venue = relationship('Venue')  # Optional if accessed via event
