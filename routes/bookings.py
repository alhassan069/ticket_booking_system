from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from models.models import Booking
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/bookings", tags=["bookings"])




"""
### Bookings:
* POST /bookings - Create new booking (requires existing event_id, venue_id, ticket_type_id)
* GET /bookings - Get all bookings with event, venue, and ticket type details
* PUT /bookings/{booking_id} - Update booking details
* DELETE /bookings/{booking_id} - Cancel a booking
* PATCH /bookings/{booking_id}/status - Update booking status (confirmed, cancelled, pending)
"""
