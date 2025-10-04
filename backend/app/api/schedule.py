from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import TimetableEvent
from app.schemas import (
    TimetableEventCreate,
    TimetableEventResponse,
    ICSImportRequest,
    ICSImportResponse
)
from app.services.ics_import import import_ics_from_url

router = APIRouter(prefix="/api/schedule", tags=["Schedule"])


@router.get("/", response_model=List[TimetableEventResponse])
async def list_schedule_events(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    start_date: str = None,
    end_date: str = None
):
    """List schedule events."""
    query = select(TimetableEvent)
    
    if start_date:
        start_dt = datetime.fromisoformat(start_date)
        query = query.where(TimetableEvent.start_time >= start_dt)
    
    if end_date:
        end_dt = datetime.fromisoformat(end_date)
        query = query.where(TimetableEvent.end_time <= end_dt)
    
    result = await db.execute(query)
    events = result.scalars().all()
    return events


@router.post("/", response_model=TimetableEventResponse)
async def create_schedule_event(
    event: TimetableEventCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new schedule event."""
    db_event = TimetableEvent(**event.model_dump())
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event


@router.delete("/{event_id}")
async def delete_schedule_event(
    event_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a schedule event."""
    result = await db.execute(
        select(TimetableEvent).where(TimetableEvent.id == event_id)
    )
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    await db.delete(event)
    await db.commit()
    return {"success": True}


@router.post("/import-ics", response_model=ICSImportResponse)
async def import_ics_schedule(
    request: ICSImportRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Import schedule from ICS file URL."""
    events_data, errors = await import_ics_from_url(request.url)
    
    imported_count = 0
    for event_data in events_data:
        try:
            event = TimetableEvent(**event_data)
            db.add(event)
            imported_count += 1
        except Exception as e:
            errors.append(f"Failed to import event: {str(e)}")
    
    await db.commit()
    
    return {
        "success": len(errors) == 0,
        "imported_count": imported_count,
        "errors": errors
    }
