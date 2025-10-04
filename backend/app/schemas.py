from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date


# Auth schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserPreferences(BaseModel):
    language: str = "fr"
    class_mode: bool = False
    theme: str = "light"

    class Config:
        from_attributes = True


# Student schemas
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    class_name: Optional[str] = None
    student_id: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    parent_name: Optional[str] = None
    parent_email: Optional[str] = None
    parent_phone: Optional[str] = None
    medical_info: Optional[str] = None


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Competence schemas
class CompetenceBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    level: Optional[str] = None


class CompetenceCreate(CompetenceBase):
    pass


class Competence(CompetenceBase):
    id: int

    class Config:
        from_attributes = True


# Evaluation schemas
class EvaluationBase(BaseModel):
    student_id: int
    competence_id: Optional[int] = None
    type: str
    value: float
    max_value: float = 20.0
    comment: Optional[str] = None
    period: Optional[str] = None
    subject: Optional[str] = None


class EvaluationCreate(EvaluationBase):
    pass


class Evaluation(EvaluationBase):
    id: int
    date: datetime
    teacher_id: int

    class Config:
        from_attributes = True


# Incident schemas
class IncidentBase(BaseModel):
    student_id: int
    type: str
    description: Optional[str] = None
    is_positive: bool = False
    points: int = 0


class IncidentCreate(IncidentBase):
    pass


class Incident(IncidentBase):
    id: int
    date: datetime
    teacher_id: int

    class Config:
        from_attributes = True


# Attendance schemas
class AttendanceBase(BaseModel):
    student_id: int
    date: datetime
    status: str
    reason: Optional[str] = None


class AttendanceCreate(AttendanceBase):
    pass


class Attendance(AttendanceBase):
    id: int
    teacher_id: int

    class Config:
        from_attributes = True


# Timetable schemas
class TimetableEventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    class_name: Optional[str] = None
    subject: Optional[str] = None
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None


class TimetableEventCreate(TimetableEventBase):
    pass


class TimetableEvent(TimetableEventBase):
    id: int
    teacher_id: Optional[int] = None

    class Config:
        from_attributes = True


# Reminder schemas
class ReminderBase(BaseModel):
    title: str
    description: Optional[str] = None
    type: str
    due_date: Optional[datetime] = None
    priority: str = "NORMAL"


class ReminderCreate(ReminderBase):
    pass


class Reminder(ReminderBase):
    id: int
    is_completed: bool
    teacher_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Seat schemas
class SeatBase(BaseModel):
    student_id: int
    class_name: Optional[str] = None
    row: int
    column: int


class SeatCreate(SeatBase):
    pass


class Seat(SeatBase):
    id: int
    teacher_id: int

    class Config:
        from_attributes = True


# Protocol schemas
class ProtocolBase(BaseModel):
    student_id: int
    type: str
    title: str
    description: Optional[str] = None
    actions: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool = True


class ProtocolCreate(ProtocolBase):
    pass


class Protocol(ProtocolBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Letter Template schemas
class LetterTemplateBase(BaseModel):
    title: str
    content: str
    type: Optional[str] = None


class LetterTemplateCreate(LetterTemplateBase):
    pass


class LetterTemplate(LetterTemplateBase):
    id: int
    created_at: datetime
    teacher_id: int

    class Config:
        from_attributes = True


# Dashboard response
class DashboardResponse(BaseModel):
    timetable_events: List[TimetableEvent]
    reminders: List[Reminder]
    incidents: List[Incident]
    upcoming_appointments: List[dict]


# Import responses
class ImportResponse(BaseModel):
    success: bool
    message: str
    imported_count: int
    errors: List[str] = []
