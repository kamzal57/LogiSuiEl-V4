from __future__ import annotations

import enum
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Column, Date, DateTime, Enum, Float, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Role(str, enum.Enum):
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"


class AttendanceStatus(str, enum.Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    LATE = "LATE"
    EXCUSED = "EXCUSED"


class BehaviourCategory(str, enum.Enum):
    LATE = "LATE"
    ABSENCE = "ABSENCE"
    TALKING = "TALKING"
    BEHAVIOUR = "BEHAVIOUR"
    FORGETFULNESS = "FORGETFULNESS"
    LACK_OF_WORK = "LACK_OF_WORK"
    POSITIVE = "POSITIVE"


class ReminderScope(str, enum.Enum):
    PERSONAL = "PERSONAL"
    CLASS = "CLASS"
    SCHOOL = "SCHOOL"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    preferences: Mapped[Optional[UserPreference]] = relationship(
        "UserPreference", back_populates="user", uselist=False, lazy="selectin"
    )
    reminders: Mapped[list[Reminder]] = relationship(
        "Reminder", back_populates="owner", lazy="selectin"
    )


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    locale: Mapped[str] = mapped_column(String(10), default="fr")
    mode_class_only: Mapped[bool] = mapped_column(Boolean, default=False)
    available_widgets: Mapped[dict] = mapped_column(JSON, default=dict)

    user: Mapped[User] = relationship("User", back_populates="preferences")


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    external_id: Mapped[Optional[str]] = mapped_column(String(128), unique=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[Optional[date]] = mapped_column(Date)
    class_name: Mapped[Optional[str]] = mapped_column(String(64))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(64))
    guardians: Mapped[dict] = mapped_column(JSON, default=dict)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    evaluations: Mapped[list[Evaluation]] = relationship("Evaluation", back_populates="student", cascade="all, delete-orphan")
    behaviour_logs: Mapped[list[BehaviourLog]] = relationship("BehaviourLog", back_populates="student", cascade="all, delete-orphan")
    attendance_logs: Mapped[list[Attendance]] = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    protocols: Mapped[list[Protocol]] = relationship("Protocol", back_populates="student", cascade="all, delete-orphan")
    seating_positions: Mapped[list[SeatingPosition]] = relationship("SeatingPosition", back_populates="student", cascade="all, delete-orphan")


class Competence(Base):
    __tablename__ = "competences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    evaluations: Mapped[list[Evaluation]] = relationship("Evaluation", back_populates="competence")


class Evaluation(Base):
    __tablename__ = "evaluations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    competence_id: Mapped[Optional[int]] = mapped_column(ForeignKey("competences.id", ondelete="SET NULL"))
    evaluator_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    score: Mapped[Optional[float]] = mapped_column(Float)
    max_score: Mapped[Optional[float]] = mapped_column(Float)
    appreciation: Mapped[Optional[str]] = mapped_column(Text)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    period: Mapped[Optional[str]] = mapped_column(String(32))

    student: Mapped[Student] = relationship("Student", back_populates="evaluations")
    competence: Mapped[Optional[Competence]] = relationship("Competence", back_populates="evaluations")


class BehaviourLog(Base):
    __tablename__ = "behaviour_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    category: Mapped[BehaviourCategory] = mapped_column(Enum(BehaviourCategory), nullable=False)
    details: Mapped[Optional[str]] = mapped_column(Text)
    is_positive: Mapped[bool] = mapped_column(Boolean, default=False)
    logged_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    student: Mapped[Student] = relationship("Student", back_populates="behaviour_logs")
    teacher: Mapped[Optional[User]] = relationship("User")


class Attendance(Base):
    __tablename__ = "attendance_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[AttendanceStatus] = mapped_column(Enum(AttendanceStatus), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    comment: Mapped[Optional[str]] = mapped_column(Text)

    student: Mapped[Student] = relationship("Student", back_populates="attendance_logs")


class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    remind_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    scope: Mapped[ReminderScope] = mapped_column(Enum(ReminderScope), default=ReminderScope.PERSONAL)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner: Mapped[User] = relationship("User", back_populates="reminders")


class TimetableEvent(Base):
    __tablename__ = "timetable_events"
    __table_args__ = (UniqueConstraint("uid", name="uq_timetable_uid"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uid: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    start_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255))
    calendar_url: Mapped[Optional[str]] = mapped_column(String(2048))


class SeatingPosition(Base):
    __tablename__ = "seating_positions"
    __table_args__ = (UniqueConstraint("row_index", "column_index", name="uq_seating_position"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    row_index: Mapped[int] = mapped_column(Integer, nullable=False)
    column_index: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    student: Mapped[Student] = relationship("Student", back_populates="seating_positions")


class Protocol(Base):
    __tablename__ = "protocols"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[Optional[str]] = mapped_column(Text)
    actions: Mapped[dict] = mapped_column(JSON, default=dict)

    student: Mapped[Student] = relationship("Student", back_populates="protocols")


class ClassAssignment(Base):
    __tablename__ = "class_assignments"
    __table_args__ = (UniqueConstraint("teacher_id", "class_name", name="uq_class_assignment"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    class_name: Mapped[str] = mapped_column(String(64), nullable=False)

    teacher: Mapped[User] = relationship("User")


class AppConfig(Base):
    __tablename__ = "app_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    school_name: Mapped[Optional[str]] = mapped_column(String(255))
    academic_year: Mapped[Optional[str]] = mapped_column(String(32))
    periods: Mapped[dict] = mapped_column(JSON, default=dict)
    timetable_settings: Mapped[dict] = mapped_column(JSON, default=dict)
    appearance: Mapped[dict] = mapped_column(JSON, default=dict)
    available_tools: Mapped[dict] = mapped_column(JSON, default=dict)
    class_mode_allowed_tools: Mapped[list[str]] = mapped_column(JSON, default=list)
    outside_class_allowed_tools: Mapped[list[str]] = mapped_column(JSON, default=list)
    locale: Mapped[Optional[str]] = mapped_column(String(10))
