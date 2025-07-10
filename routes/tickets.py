from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from models.models import TicketType
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/tickets", tags=["tickets"])




"""
### Ticket Types:
* POST /ticket-types - Create new ticket type (VIP, Standard, Economy)
* GET /ticket-types - Get all ticket types
* GET /ticket-types/{type_id}/bookings - Get all bookings for a specific ticket type
"""


