from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field

from .models import AttendanceStatus, BehaviourCategory, ReminderScope, Role


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    sub: str | None = None
    role: Role | None = None
    exp: int | None = None
    type: str | None = None


class RefreshRequest(BaseModel):
    refresh_token: str


class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Role


class UserPreferences(BaseModel):
    locale: str = Field(default="fr", max_length=10)
    mode_class_only: bool = False
    available_widgets: Dict[str, bool] = Field(default_factory=dict)


class UserRead(UserBase):
    id: int
    is_active: bool
    preferences: Optional[UserPreferences]

    class Config:
        from_attributes = True


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    class_name: Optional[str] = None
    birth_date: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    guardians: Dict[str, Any] = Field(default_factory=dict)
    notes: Optional[str] = None


class StudentCreate(StudentBase):
    external_id: Optional[str] = None


class StudentUpdate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: int
    external_id: Optional[str]

    class Config:
        from_attributes = True


class CompetenceBase(BaseModel):
    code: str
    title: str
    description: Optional[str] = None


class CompetenceCreate(CompetenceBase):
    pass


class CompetenceRead(CompetenceBase):
    id: int

    class Config:
        from_attributes = True


class EvaluationBase(BaseModel):
    student_id: int
    competence_id: Optional[int] = None
    score: Optional[float] = None
    max_score: Optional[float] = None
    appreciation: Optional[str] = None
    period: Optional[str] = None


class EvaluationCreate(EvaluationBase):
    evaluated_at: Optional[datetime] = None


class EvaluationRead(EvaluationBase):
    id: int
    evaluator_id: Optional[int]
    evaluated_at: datetime

    class Config:
        from_attributes = True


class BehaviourLogBase(BaseModel):
    student_id: int
    category: BehaviourCategory
    details: Optional[str] = None
    is_positive: bool = False


class BehaviourLogCreate(BehaviourLogBase):
    pass


class BehaviourLogRead(BehaviourLogBase):
    id: int
    teacher_id: Optional[int]
    logged_at: datetime

    class Config:
        from_attributes = True


class AttendanceBase(BaseModel):
    student_id: int
    status: AttendanceStatus
    comment: Optional[str] = None


class AttendanceCreate(AttendanceBase):
    occurred_at: Optional[datetime] = None


class AttendanceRead(AttendanceBase):
    id: int
    occurred_at: datetime

    class Config:
        from_attributes = True


class ReminderBase(BaseModel):
    title: str
    description: Optional[str] = None
    remind_at: Optional[datetime] = None
    scope: ReminderScope = ReminderScope.PERSONAL


class ReminderCreate(ReminderBase):
    pass


class ReminderRead(ReminderBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class TimetableEventRead(BaseModel):
    id: int
    uid: str
    title: str
    description: Optional[str]
    start_at: datetime
    end_at: datetime
    location: Optional[str]

    class Config:
        from_attributes = True


class TimetableImportRequest(BaseModel):
    url: str = Field(..., description="URL vers le fichier ICS")


class SeatingPositionBase(BaseModel):
    student_id: int
    row_index: int
    column_index: int
    notes: Optional[str] = None


class SeatingPositionRead(SeatingPositionBase):
    id: int

    class Config:
        from_attributes = True


class ProtocolBase(BaseModel):
    student_id: int
    name: str
    details: Optional[str] = None
    actions: Dict[str, Any] = Field(default_factory=dict)


class ProtocolRead(ProtocolBase):
    id: int

    class Config:
        from_attributes = True


class DashboardColumn(BaseModel):
    label: str
    items: List[Dict[str, Any]]


class DashboardResponse(BaseModel):
    timetable: List[TimetableEventRead]
    reminders: List[ReminderRead]
    incidents: List[BehaviourLogRead]


class ReportResponse(BaseModel):
    filename: str
    content_type: str
    data: str


class ConfigPayload(BaseModel):
    school_name: Optional[str] = None
    academic_year: Optional[str] = None
    periods: List[Dict[str, Any]] = Field(default_factory=list)
    timetable_settings: Dict[str, Any] = Field(default_factory=dict)
    appearance: Dict[str, Any] = Field(default_factory=dict)
    available_tools: Dict[str, bool] = Field(default_factory=dict)
    class_mode_allowed_tools: List[str] = Field(default_factory=list)
    outside_class_allowed_tools: List[str] = Field(default_factory=list)
    locale: Optional[str] = None


class ConfigRead(ConfigPayload):
    id: int

    class Config:
        from_attributes = True


class CSVImportSummary(BaseModel):
    inserted: int
    updated: int
    skipped: int


class ICSImportSummary(BaseModel):
    events_imported: int
    calendar_url: str
