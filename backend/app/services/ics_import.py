import httpx
from ics import Calendar
from typing import List, Dict
from datetime import datetime


async def download_ics_file(url: str) -> str:
    """Download ICS file from URL."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


def parse_ics_content(content: str) -> List[Dict]:
    """Parse ICS content and extract events."""
    calendar = Calendar(content)
    events = []
    errors = []
    
    for event in calendar.events:
        try:
            event_data = {
                "title": event.name,
                "description": event.description or "",
                "start_time": event.begin.datetime if event.begin else None,
                "end_time": event.end.datetime if event.end else None,
                "location": event.location or "",
                "event_type": "course"
            }
            events.append(event_data)
        except Exception as e:
            errors.append(f"Event parsing error: {str(e)}")
    
    return events, errors


async def import_ics_from_url(url: str) -> tuple[List[Dict], List[str]]:
    """Download and parse ICS file from URL."""
    try:
        content = await download_ics_file(url)
        events, errors = parse_ics_content(content)
        return events, errors
    except Exception as e:
        return [], [f"Failed to download ICS file: {str(e)}"]
