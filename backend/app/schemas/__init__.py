# Schemas initialization
from app.schemas.auth import (
    Token, TokenData, UserBase, UserCreate, UserUpdate, 
    UserInDB, UserResponse, UserPreferencesBase, 
    UserPreferencesUpdate, UserPreferencesResponse
)
from app.schemas.schemas import (
    StudentBase, StudentCreate, StudentUpdate, StudentResponse,
    CompetenceBase, CompetenceCreate, CompetenceUpdate, CompetenceResponse,
    EvaluationBase, EvaluationCreate, EvaluationUpdate, EvaluationResponse,
    IncidentBase, IncidentCreate, IncidentUpdate, IncidentResponse,
    AttendanceBase, AttendanceCreate, AttendanceUpdate, AttendanceResponse,
    SeatBase, SeatCreate, SeatUpdate, SeatResponse,
    ProtocolBase, ProtocolCreate, ProtocolUpdate, ProtocolResponse,
    TimetableEventBase, TimetableEventCreate, TimetableEventUpdate, TimetableEventResponse,
    ReminderBase, ReminderCreate, ReminderUpdate, ReminderResponse
)

__all__ = [
    "Token", "TokenData", "UserBase", "UserCreate", "UserUpdate", 
    "UserInDB", "UserResponse", "UserPreferencesBase",
    "UserPreferencesUpdate", "UserPreferencesResponse",
    "StudentBase", "StudentCreate", "StudentUpdate", "StudentResponse",
    "CompetenceBase", "CompetenceCreate", "CompetenceUpdate", "CompetenceResponse",
    "EvaluationBase", "EvaluationCreate", "EvaluationUpdate", "EvaluationResponse",
    "IncidentBase", "IncidentCreate", "IncidentUpdate", "IncidentResponse",
    "AttendanceBase", "AttendanceCreate", "AttendanceUpdate", "AttendanceResponse",
    "SeatBase", "SeatCreate", "SeatUpdate", "SeatResponse",
    "ProtocolBase", "ProtocolCreate", "ProtocolUpdate", "ProtocolResponse",
    "TimetableEventBase", "TimetableEventCreate", "TimetableEventUpdate", "TimetableEventResponse",
    "ReminderBase", "ReminderCreate", "ReminderUpdate", "ReminderResponse"
]
