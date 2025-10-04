from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..dependencies import get_current_active_teacher
from ..models import BehaviourLog, Reminder, ReminderScope, TimetableEvent, User
from ..schemas import BehaviourLogRead, DashboardResponse, ReminderRead, TimetableEventRead

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_teacher),
) -> DashboardResponse:
    now = datetime.utcnow()
    week_limit = now + timedelta(days=7)

    timetable_result = await db.execute(
        select(TimetableEvent)
        .where(TimetableEvent.start_at >= now, TimetableEvent.start_at <= week_limit)
        .order_by(TimetableEvent.start_at)
    )
    timetable_items = [
        TimetableEventRead.model_validate(event, from_attributes=True)
        for event in timetable_result.scalars().all()
    ]

    reminder_stmt = select(Reminder)
    if current_user.role.name != "ADMIN":
        reminder_stmt = reminder_stmt.where(
            or_(
                Reminder.owner_id == current_user.id,
                Reminder.scope.in_([ReminderScope.CLASS, ReminderScope.SCHOOL]),
            )
        )
    reminder_stmt = reminder_stmt.order_by(Reminder.remind_at.desc().nullslast())
    reminder_result = await db.execute(reminder_stmt.limit(20))
    reminders = [
        ReminderRead.model_validate(reminder, from_attributes=True)
        for reminder in reminder_result.scalars().all()
    ]

    incidents_result = await db.execute(
        select(BehaviourLog)
        .order_by(BehaviourLog.logged_at.desc())
        .limit(20)
    )
    incidents = [
        BehaviourLogRead.model_validate(log, from_attributes=True)
        for log in incidents_result.scalars().all()
    ]

    return DashboardResponse(timetable=timetable_items, reminders=reminders, incidents=incidents)
