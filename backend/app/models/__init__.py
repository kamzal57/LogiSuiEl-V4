# Models initialization
from app.models.user import User, Role
from app.models.models import (
    Student, Competence, Evaluation, Incident, Attendance,
    Seat, Protocol, TimetableEvent, Reminder, UserPreferences
)

__all__ = [
    "User", "Role",
    "Student", "Competence", "Evaluation", "Incident", "Attendance",
    "Seat", "Protocol", "TimetableEvent", "Reminder", "UserPreferences"
]
