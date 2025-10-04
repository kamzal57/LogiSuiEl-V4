from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Reminder
from app.schemas import ReminderCreate, ReminderUpdate, ReminderResponse

router = APIRouter(prefix="/api/reminders", tags=["Reminders"])


@router.get("/", response_model=List[ReminderResponse])
async def list_reminders(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List user's reminders."""
    result = await db.execute(
        select(Reminder).where(Reminder.user_id == current_user.id)
    )
    reminders = result.scalars().all()
    return reminders


@router.post("/", response_model=ReminderResponse)
async def create_reminder(
    reminder: ReminderCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new reminder."""
    db_reminder = Reminder(**reminder.model_dump(), user_id=current_user.id)
    db.add(db_reminder)
    await db.commit()
    await db.refresh(db_reminder)
    return db_reminder


@router.put("/{reminder_id}", response_model=ReminderResponse)
async def update_reminder(
    reminder_id: int,
    reminder_update: ReminderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update a reminder."""
    result = await db.execute(
        select(Reminder).where(
            Reminder.id == reminder_id,
            Reminder.user_id == current_user.id
        )
    )
    reminder = result.scalar_one_or_none()
    
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    for key, value in reminder_update.model_dump(exclude_unset=True).items():
        setattr(reminder, key, value)
    
    await db.commit()
    await db.refresh(reminder)
    return reminder


@router.delete("/{reminder_id}")
async def delete_reminder(
    reminder_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a reminder."""
    result = await db.execute(
        select(Reminder).where(
            Reminder.id == reminder_id,
            Reminder.user_id == current_user.id
        )
    )
    reminder = result.scalar_one_or_none()
    
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    await db.delete(reminder)
    await db.commit()
    return {"success": True}
