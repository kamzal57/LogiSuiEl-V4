import requests
from ics import Calendar
from datetime import datetime
from sqlalchemy.orm import Session
from .. import models


def import_ics_from_url(url: str, teacher_id: int, db: Session) -> dict:
    """Download and import ICS file from URL"""
    errors = []
    imported_count = 0
    
    try:
        # Download the ICS file
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Parse the ICS content
        calendar = Calendar(response.text)
        
        for event in calendar.events:
            try:
                # Create timetable event
                db_event = models.TimetableEvent(
                    title=event.name or "Untitled Event",
                    description=event.description or "",
                    start_time=event.begin.datetime,
                    end_time=event.end.datetime,
                    location=event.location or "",
                    teacher_id=teacher_id
                )
                db.add(db_event)
                imported_count += 1
            except Exception as e:
                errors.append(f"Event '{event.name}': {str(e)}")
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Successfully imported {imported_count} events",
            "imported_count": imported_count,
            "errors": errors
        }
    except requests.RequestException as e:
        return {
            "success": False,
            "message": f"Failed to download ICS file: {str(e)}",
            "imported_count": 0,
            "errors": [str(e)]
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "message": f"Failed to import ICS: {str(e)}",
            "imported_count": 0,
            "errors": [str(e)]
        }
