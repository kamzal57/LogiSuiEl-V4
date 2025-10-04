import requests
from ics import Calendar
from datetime import datetime
from typing import List, Dict, Any

def download_and_parse_ics(url: str) -> List[Dict[str, Any]]:
    """Download ICS file from URL and parse events"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        calendar = Calendar(response.text)
        events = []
        
        for event in calendar.events:
            event_data = {
                'title': event.name,
                'start_time': event.begin.datetime if hasattr(event.begin, 'datetime') else event.begin,
                'end_time': event.end.datetime if hasattr(event.end, 'datetime') else event.end,
                'location': event.location if event.location else None,
                'notes': event.description if event.description else None,
                'is_recurring': False  # Basic implementation, can be enhanced
            }
            
            # Extract day of week from start time
            if isinstance(event_data['start_time'], datetime):
                event_data['day_of_week'] = event_data['start_time'].weekday()
            
            events.append(event_data)
        
        return events
    except Exception as e:
        raise ValueError(f"Failed to download or parse ICS file: {str(e)}")
