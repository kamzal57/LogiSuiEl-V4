from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..dependencies import get_current_admin, get_current_active_teacher
from ..models import TimetableEvent, User
from ..schemas import ICSImportSummary, TimetableEventRead, TimetableImportRequest
from ..services.ics_import import import_ics_calendar

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.post("/import-ics", response_model=ICSImportSummary)
async def import_ics(
    payload: TimetableImportRequest,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> ICSImportSummary:
    try:
        summary = await import_ics_calendar(payload.url, db)
    except Exception as exc:  # pragma: no cover - httpx will provide detail
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return summary


@router.get("/events", response_model=List[TimetableEventRead])
async def list_events(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_active_teacher),
) -> List[TimetableEventRead]:
    result = await db.execute(select(TimetableEvent).order_by(TimetableEvent.start_at))
    events = result.scalars().all()
    return [TimetableEventRead.model_validate(event, from_attributes=True) for event in events]
