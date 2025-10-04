from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ..core.database import get_db
from ..core.security import get_current_user
from .. import models, schemas

router = APIRouter(prefix="/api/schedule", tags=["schedule"])


@router.get("/", response_model=List[schemas.TimetableEvent])
async def get_schedule(
    start_date: str = None,
    end_date: str = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get schedule/timetable events"""
    query = db.query(models.TimetableEvent).filter(
        models.TimetableEvent.teacher_id == current_user.id
    )
    
    if start_date:
        start = datetime.fromisoformat(start_date)
        query = query.filter(models.TimetableEvent.start_time >= start)
    
    if end_date:
        end = datetime.fromisoformat(end_date)
        query = query.filter(models.TimetableEvent.end_time <= end)
    
    events = query.order_by(models.TimetableEvent.start_time).all()
    return events


@router.post("/", response_model=schemas.TimetableEvent)
async def create_event(
    event: schemas.TimetableEventCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new schedule event"""
    db_event = models.TimetableEvent(**event.dict(), teacher_id=current_user.id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.post("/import-ics", response_model=schemas.ImportResponse)
async def import_ics(
    url: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Import schedule from ICS file URL"""
    from ..services.ics import import_ics_from_url
    
    result = import_ics_from_url(url, current_user.id, db)
    return result


@router.delete("/{event_id}")
async def delete_event(
    event_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a schedule event"""
    event = db.query(models.TimetableEvent).filter(
        models.TimetableEvent.id == event_id,
        models.TimetableEvent.teacher_id == current_user.id
    ).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(event)
    db.commit()
    return {"message": "Event deleted successfully"}
