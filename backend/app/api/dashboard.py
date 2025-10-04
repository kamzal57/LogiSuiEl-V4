from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import TimetableEvent, Reminder, Incident
from app.schemas import DashboardResponse

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/", response_model=DashboardResponse)
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get dashboard data with schedule, reminders, and recent incidents."""
    # Get upcoming schedule events (next 7 days)
    now = datetime.utcnow()
    week_later = now + timedelta(days=7)
    
    result = await db.execute(
        select(TimetableEvent)
        .where(TimetableEvent.start_time >= now)
        .where(TimetableEvent.start_time <= week_later)
        .order_by(TimetableEvent.start_time)
        .limit(20)
    )
    timetable_events = result.scalars().all()
    
    # Get active reminders
    result = await db.execute(
        select(Reminder)
        .where(Reminder.user_id == current_user.id)
        .where(Reminder.completed == False)
        .order_by(Reminder.due_date)
        .limit(20)
    )
    reminders = result.scalars().all()
    
    # Get recent incidents (last 7 days)
    week_ago = now - timedelta(days=7)
    result = await db.execute(
        select(Incident)
        .where(Incident.date >= week_ago)
        .order_by(Incident.date.desc())
        .limit(20)
    )
    recent_incidents = result.scalars().all()
    
    return {
        "timetable_events": timetable_events,
        "reminders": reminders,
        "recent_incidents": recent_incidents
    }
