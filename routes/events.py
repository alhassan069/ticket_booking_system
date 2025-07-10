from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from models.models import Event, Venue
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/events", tags=["events"])



"""
### Events:
* POST /events - Create new event -- DONE
* GET /events - Get all events
* GET /events/{event_id}/bookings - Get all bookings for a specific event
* GET /events/{event_id}/available-tickets - Get available tickets for an event

"""



class EventCreateEdit(BaseModel):
    name: str
    description: Optional[str] = None
    venue_id: int
    start_time: datetime
    end_time: datetime

class EventResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    venue_id: int
    start_time: datetime
    end_time: datetime
    created_at: datetime

    model_config = {"from_attributes": True}





@router.post("/")
def create_event(event: EventCreateEdit, db: Session = Depends(get_db)) -> EventResponse:
    '''
    Create a new event
    '''
    new_event = Event(name=event.name, description=event.description, venue_id=event.venue_id, start_time=event.start_time, end_time=event.end_time)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return EventResponse.model_validate(new_event)
