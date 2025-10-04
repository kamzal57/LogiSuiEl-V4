from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models import User, TimetableEvent
from app.schemas import (
    TimetableEventCreate, TimetableEventUpdate, TimetableEventResponse
)
from app.services.ics_import import download_and_parse_ics

router = APIRouter()

@router.get("/", response_model=List[TimetableEventResponse])
async def get_timetable_events(
    week_type: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get timetable events, optionally filtered by week type (A/B)"""
    query = db.query(TimetableEvent)
    
    if week_type:
        query = query.filter(
            (TimetableEvent.week_type == week_type) | 
            (TimetableEvent.week_type == None)
        )
    
    events = query.order_by(TimetableEvent.day_of_week, TimetableEvent.start_time).all()
    return events

@router.post("/", response_model=TimetableEventResponse)
async def create_timetable_event(
    event: TimetableEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    """Create a new timetable event"""
    db_event = TimetableEvent(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.put("/{event_id}", response_model=TimetableEventResponse)
async def update_timetable_event(
    event_id: int,
    event: TimetableEventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    """Update a timetable event"""
    db_event = db.query(TimetableEvent).filter(TimetableEvent.id == event_id).first()
    
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    update_data = event.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/{event_id}")
async def delete_timetable_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    """Delete a timetable event"""
    db_event = db.query(TimetableEvent).filter(TimetableEvent.id == event_id).first()
    
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted successfully"}

@router.post("/import-ics")
async def import_from_ics(
    url: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    """Import timetable events from ICS URL"""
    try:
        events_data = download_and_parse_ics(url)
        
        imported_count = 0
        for event_data in events_data:
            db_event = TimetableEvent(**event_data)
            db.add(db_event)
            imported_count += 1
        
        db.commit()
        
        return {
            "message": f"Successfully imported {imported_count} events",
            "count": imported_count
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to import ICS: {str(e)}"
        )
