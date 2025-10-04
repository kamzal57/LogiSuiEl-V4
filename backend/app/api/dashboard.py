from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ..core.database import get_db
from ..core.security import get_current_user
from .. import models, schemas

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/", response_model=schemas.DashboardResponse)
async def get_dashboard(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard data"""
    # Get timetable for the current week
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=7)
    
    timetable_events = db.query(models.TimetableEvent).filter(
        models.TimetableEvent.teacher_id == current_user.id,
        models.TimetableEvent.start_time >= week_start,
        models.TimetableEvent.start_time <= week_end
    ).order_by(models.TimetableEvent.start_time).all()
    
    # Get active reminders
    reminders = db.query(models.Reminder).filter(
        models.Reminder.teacher_id == current_user.id,
        models.Reminder.is_completed == False
    ).order_by(models.Reminder.due_date).limit(10).all()
    
    # Get recent incidents
    incidents = db.query(models.Incident).filter(
        models.Incident.teacher_id == current_user.id
    ).order_by(models.Incident.date.desc()).limit(20).all()
    
    # Upcoming appointments (from reminders)
    upcoming = []
    for reminder in reminders:
        if reminder.type in ["RDV_PARENT", "REUNION", "APPEL"] and reminder.due_date:
            upcoming.append({
                "id": reminder.id,
                "title": reminder.title,
                "date": reminder.due_date,
                "type": reminder.type
            })
    
    return {
        "timetable_events": timetable_events,
        "reminders": reminders,
        "incidents": incidents,
        "upcoming_appointments": upcoming
    }


@router.get("/reminders", response_model=List[schemas.Reminder])
async def get_reminders(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all reminders"""
    reminders = db.query(models.Reminder).filter(
        models.Reminder.teacher_id == current_user.id
    ).order_by(models.Reminder.due_date).all()
    return reminders


@router.post("/reminders", response_model=schemas.Reminder)
async def create_reminder(
    reminder: schemas.ReminderCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new reminder"""
    db_reminder = models.Reminder(**reminder.dict(), teacher_id=current_user.id)
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder


@router.put("/reminders/{reminder_id}", response_model=schemas.Reminder)
async def update_reminder(
    reminder_id: int,
    reminder: schemas.ReminderCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a reminder"""
    db_reminder = db.query(models.Reminder).filter(
        models.Reminder.id == reminder_id,
        models.Reminder.teacher_id == current_user.id
    ).first()
    
    if not db_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    for key, value in reminder.dict().items():
        setattr(db_reminder, key, value)
    
    db.commit()
    db.refresh(db_reminder)
    return db_reminder


@router.delete("/reminders/{reminder_id}")
async def delete_reminder(
    reminder_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a reminder"""
    db_reminder = db.query(models.Reminder).filter(
        models.Reminder.id == reminder_id,
        models.Reminder.teacher_id == current_user.id
    ).first()
    
    if not db_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    db.delete(db_reminder)
    db.commit()
    return {"message": "Reminder deleted successfully"}
