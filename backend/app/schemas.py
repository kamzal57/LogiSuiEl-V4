from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr


# User schemas
class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Student schemas
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    class_name: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    parent_contact: Optional[str] = None
    email: Optional[EmailStr] = None
    notes: Optional[str] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    class_name: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    parent_contact: Optional[str] = None
    email: Optional[EmailStr] = None
    notes: Optional[str] = None


class StudentResponse(StudentBase):
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


class CompetenceCreate(CompetenceBase):
    pass


class CompetenceResponse(CompetenceBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Evaluation schemas
class EvaluationBase(BaseModel):
    student_id: int
    competence_id: Optional[int] = None
    type: str
    value: Optional[float] = None
    grade: Optional[str] = None
    comment: Optional[str] = None
    period: Optional[str] = None


class EvaluationCreate(EvaluationBase):
    pass


class EvaluationResponse(EvaluationBase):
    id: int
    date: datetime
    
    class Config:
        from_attributes = True


# Incident schemas
class IncidentBase(BaseModel):
    student_id: int
    type: str
    is_positive: bool = False
    description: Optional[str] = None
    severity: int = 1


class IncidentCreate(IncidentBase):
    pass


class IncidentResponse(IncidentBase):
    id: int
    date: datetime
    
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


class AttendanceResponse(AttendanceBase):
    id: int
    
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
    event_type: Optional[str] = None
    recurrence: Optional[str] = None


class TimetableEventCreate(TimetableEventBase):
    pass


class TimetableEventResponse(TimetableEventBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Reminder schemas
class ReminderBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: int = 1
    category: Optional[str] = None


class ReminderCreate(ReminderBase):
    pass


class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None
    category: Optional[str] = None


class ReminderResponse(ReminderBase):
    id: int
    user_id: Optional[int] = None
    completed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Seat assignment schemas
class SeatAssignmentBase(BaseModel):
    student_id: int
    class_name: Optional[str] = None
    row: Optional[int] = None
    column: Optional[int] = None


class SeatAssignmentCreate(SeatAssignmentBase):
    pass


class SeatAssignmentResponse(SeatAssignmentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Protocol schemas
class ProtocolBase(BaseModel):
    student_id: int
    type: str
    title: str
    description: Optional[str] = None
    actions: Optional[List[Any]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ProtocolCreate(ProtocolBase):
    pass


class ProtocolResponse(ProtocolBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# App config schemas
class AppConfigBase(BaseModel):
    key: str
    value: Any
    description: Optional[str] = None


class AppConfigCreate(AppConfigBase):
    pass


class AppConfigResponse(AppConfigBase):
    id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Letter template schemas
class LetterTemplateBase(BaseModel):
    name: str
    category: Optional[str] = None
    content: str
    variables: Optional[List[str]] = None


class LetterTemplateCreate(LetterTemplateBase):
    pass


class LetterTemplateResponse(LetterTemplateBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Dashboard schemas
class DashboardResponse(BaseModel):
    timetable_events: List[TimetableEventResponse]
    reminders: List[ReminderResponse]
    recent_incidents: List[IncidentResponse]
    
    class Config:
        from_attributes = True


# Import schemas
class CSVImportResponse(BaseModel):
    success: bool
    imported_count: int
    errors: List[str] = []


class ICSImportRequest(BaseModel):
    url: str


class ICSImportResponse(BaseModel):
    success: bool
    imported_count: int
    errors: List[str] = []
