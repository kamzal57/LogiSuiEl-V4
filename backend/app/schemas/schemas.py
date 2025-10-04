from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date

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

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    class_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    parent_name: Optional[str] = None
    parent_email: Optional[str] = None
    parent_phone: Optional[str] = None

class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Competence schemas
class CompetenceBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    level: Optional[int] = None

class CompetenceCreate(CompetenceBase):
    pass

class CompetenceUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    level: Optional[int] = None

class CompetenceResponse(CompetenceBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Evaluation schemas
class EvaluationBase(BaseModel):
    student_id: int
    competence_id: int
    score: Optional[float] = None
    note: Optional[str] = None
    period: Optional[str] = None
    comment: Optional[str] = None

class EvaluationCreate(EvaluationBase):
    pass

class EvaluationUpdate(BaseModel):
    score: Optional[float] = None
    note: Optional[str] = None
    period: Optional[str] = None
    comment: Optional[str] = None

class EvaluationResponse(EvaluationBase):
    id: int
    evaluation_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# Incident schemas
class IncidentBase(BaseModel):
    student_id: int
    type: str
    description: Optional[str] = None
    severity: Optional[int] = Field(None, ge=1, le=5)

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(BaseModel):
    type: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[int] = Field(None, ge=1, le=5)
    resolved: Optional[bool] = None
    resolution_note: Optional[str] = None

class IncidentResponse(IncidentBase):
    id: int
    date: datetime
    resolved: bool
    resolution_note: Optional[str] = None
    created_by: Optional[int] = None
    
    class Config:
        from_attributes = True

# Attendance schemas
class AttendanceBase(BaseModel):
    student_id: int
    date: date
    status: str
    minutes_late: Optional[int] = None
    note: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    status: Optional[str] = None
    minutes_late: Optional[int] = None
    note: Optional[str] = None

class AttendanceResponse(AttendanceBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Seat schemas
class SeatBase(BaseModel):
    student_id: int
    class_name: str
    row: int
    column: int

class SeatCreate(SeatBase):
    pass

class SeatUpdate(BaseModel):
    row: Optional[int] = None
    column: Optional[int] = None

class SeatResponse(SeatBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
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

class ProtocolUpdate(BaseModel):
    type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    actions: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None

class ProtocolResponse(ProtocolBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Timetable schemas
class TimetableEventBase(BaseModel):
    title: str
    class_name: Optional[str] = None
    location: Optional[str] = None
    start_time: datetime
    end_time: datetime
    day_of_week: Optional[int] = None
    week_type: Optional[str] = None
    is_recurring: bool = False
    color: Optional[str] = None
    notes: Optional[str] = None

class TimetableEventCreate(TimetableEventBase):
    pass

class TimetableEventUpdate(BaseModel):
    title: Optional[str] = None
    class_name: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    day_of_week: Optional[int] = None
    week_type: Optional[str] = None
    is_recurring: Optional[bool] = None
    color: Optional[str] = None
    notes: Optional[str] = None

class TimetableEventResponse(TimetableEventBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Reminder schemas
class ReminderBase(BaseModel):
    title: str
    description: Optional[str] = None
    type: str
    due_date: Optional[datetime] = None
    priority: int = Field(1, ge=1, le=5)

class ReminderCreate(ReminderBase):
    pass

class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None
    priority: Optional[int] = Field(None, ge=1, le=5)

class ReminderResponse(ReminderBase):
    id: int
    user_id: int
    is_completed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
