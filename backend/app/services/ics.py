import requests
from datetime import datetime
from sqlalchemy.orm import Session
from .. import models


def parse_ics_date(date_str: str) -> datetime:
    """Parse ICS datetime string"""
    # ICS format: YYYYMMDDTHHMMSS or YYYYMMDDTHHMMSSZ
    date_str = date_str.replace('Z', '').replace('T', '')
    if len(date_str) >= 14:
        return datetime.strptime(date_str[:14], '%Y%m%d%H%M%S')
    elif len(date_str) >= 8:
        return datetime.strptime(date_str[:8], '%Y%m%d')
    return datetime.now()


def import_ics_from_url(url: str, teacher_id: int, db: Session) -> dict:
    """Download and import ICS file from URL"""
    errors = []
    imported_count = 0
    
    try:
        # Download the ICS file
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Simple ICS parser
        lines = response.text.split('\n')
        current_event = {}
        in_event = False
        
        for line in lines:
            line = line.strip()
            
            if line == 'BEGIN:VEVENT':
                in_event = True
                current_event = {}
            elif line == 'END:VEVENT' and in_event:
                in_event = False
                try:
                    # Create timetable event
                    db_event = models.TimetableEvent(
                        title=current_event.get('SUMMARY', 'Untitled Event'),
                        description=current_event.get('DESCRIPTION', ''),
                        start_time=parse_ics_date(current_event.get('DTSTART', '')),
                        end_time=parse_ics_date(current_event.get('DTEND', '')),
                        location=current_event.get('LOCATION', ''),
                        teacher_id=teacher_id
                    )
                    db.add(db_event)
                    imported_count += 1
                except Exception as e:
                    errors.append(f"Event error: {str(e)}")
            elif in_event and ':' in line:
                key, value = line.split(':', 1)
                current_event[key] = value
        
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
