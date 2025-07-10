from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from models.models import Venue
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/venues", tags=["venues"])

class VenueCreateEdit(BaseModel):
    name: str
    location: str
    capacity: int

class VenueResponse(BaseModel):
    id: int
    name: str
    location: str
    capacity: int
    created_at: datetime
    model_config = {"from_attributes": True}


"""
### Venues:
* POST /venues - Create new venue -- DONE
* GET /venues - Get all venues -- DONE
* GET /venues/{venue_id}/events - Get all events at a specific venue --TBD
"""

@router.post("/")
def create_venue(venue: VenueCreateEdit, db: Session = Depends(get_db)) -> VenueResponse:
    '''
    Create a new venue
    '''
    new_venue = Venue(name=venue.name, location=venue.location, capacity=venue.capacity)
    db.add(new_venue)
    db.commit()
    db.refresh(new_venue)
    return VenueResponse.model_validate(new_venue)

@router.get("/")
def get_venues(db: Session = Depends(get_db)) -> list[VenueResponse]:
    '''
    Get all venues
    '''
    venues = db.query(Venue).all()
    return [VenueResponse.model_validate(venue) for venue in venues]
