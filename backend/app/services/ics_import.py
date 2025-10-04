from __future__ import annotations

from datetime import datetime

import httpx
from ics import Calendar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import TimetableEvent
from ..schemas import ICSImportSummary


async def import_ics_calendar(url: str, session: AsyncSession) -> ICSImportSummary:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.text

    calendar = Calendar(data)

    imported = 0

    for event in calendar.events:
        uid = event.uid or f"{event.name}-{event.begin}"  # fallback
        result = await session.execute(select(TimetableEvent).where(TimetableEvent.uid == uid))
        timetable_event = result.scalar_one_or_none()

        start_at = event.begin.datetime if hasattr(event.begin, "datetime") else event.begin
        end_at = event.end.datetime if hasattr(event.end, "datetime") else event.end

        if isinstance(start_at, datetime) and start_at.tzinfo:
            start_at = start_at.astimezone(tz=None).replace(tzinfo=None)
        if isinstance(end_at, datetime) and end_at.tzinfo:
            end_at = end_at.astimezone(tz=None).replace(tzinfo=None)

        payload = {
            "uid": uid,
            "title": event.name or "Cours",
            "description": event.description or "",
            "start_at": start_at,
            "end_at": end_at,
            "location": event.location,
            "calendar_url": url,
        }

        if timetable_event:
            for key, value in payload.items():
                setattr(timetable_event, key, value)
        else:
            session.add(TimetableEvent(**payload))
        imported += 1

    await session.commit()

    return ICSImportSummary(events_imported=imported, calendar_url=url)
