from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, TimetableEvent, Reminder, Incident
from app.schemas import TimetableEventResponse, ReminderResponse, IncidentResponse

router = APIRouter()

@router.get("/")
async def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard data including timetable, reminders, and recent incidents"""
    
    # Get current week's timetable events
    now = datetime.utcnow()
    current_day = now.weekday()
    
    timetable_events = db.query(TimetableEvent).filter(
        TimetableEvent.start_time >= now
    ).order_by(TimetableEvent.start_time).limit(20).all()
    
    # Get upcoming reminders
    reminders = db.query(Reminder).filter(
        Reminder.user_id == current_user.id,
        Reminder.is_completed == False
    ).order_by(Reminder.due_date).limit(10).all()
    
    # Get recent unresolved incidents
    recent_incidents = db.query(Incident).filter(
        Incident.resolved == False
    ).order_by(Incident.date.desc()).limit(10).all()
    
    return {
        "timetable": [TimetableEventResponse.model_validate(event) for event in timetable_events],
        "reminders": [ReminderResponse.model_validate(reminder) for reminder in reminders],
        "recent_incidents": [IncidentResponse.model_validate(incident) for incident in recent_incidents]
    }
