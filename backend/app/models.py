from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, Text, JSON
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """User model for authentication."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # ADMIN or TEACHER
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    preferences = relationship("UserPreferences", back_populates="user", uselist=False)


class UserPreferences(Base):
    """User preferences and settings."""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    class_mode = Column(Boolean, default=False)
    language = Column(String, default="fr")
    theme = Column(String, default="light")
    widgets_enabled = Column(JSON, default=list)
    
    user = relationship("User", back_populates="preferences")


class Student(Base):
    """Student model."""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    class_name = Column(String)
    date_of_birth = Column(DateTime)
    parent_contact = Column(String)
    email = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    evaluations = relationship("Evaluation", back_populates="student")
    incidents = relationship("Incident", back_populates="student")
    attendances = relationship("Attendance", back_populates="student")
    seat_assignment = relationship("SeatAssignment", back_populates="student", uselist=False)


class Competence(Base):
    """Competence/Skill model."""
    __tablename__ = "competences"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    evaluations = relationship("Evaluation", back_populates="competence")


class Evaluation(Base):
    """Evaluation/Grade model."""
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    competence_id = Column(Integer, ForeignKey("competences.id"))
    type = Column(String)  # competence, note, bilan
    value = Column(Float)
    grade = Column(String)
    comment = Column(Text)
    date = Column(DateTime, default=datetime.utcnow)
    period = Column(String)
    
    student = relationship("Student", back_populates="evaluations")
    competence = relationship("Competence", back_populates="evaluations")


class Incident(Base):
    """Incident model for behavior tracking."""
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    type = Column(String, nullable=False)  # retard, absence, bavardage, comportement, oubli, travail, participation
    is_positive = Column(Boolean, default=False)
    description = Column(Text)
    date = Column(DateTime, default=datetime.utcnow)
    severity = Column(Integer, default=1)
    
    student = relationship("Student", back_populates="incidents")


class Attendance(Base):
    """Attendance tracking."""
    __tablename__ = "attendances"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)  # present, absent, late
    reason = Column(Text)
    
    student = relationship("Student", back_populates="attendances")


class TimetableEvent(Base):
    """Timetable/Schedule event."""
    __tablename__ = "timetable_events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String)
    class_name = Column(String)
    event_type = Column(String)  # course, reunion, retenue, etc.
    recurrence = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Reminder(Base):
    """Reminder/Todo model."""
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    description = Column(Text)
    due_date = Column(DateTime)
    priority = Column(Integer, default=1)
    completed = Column(Boolean, default=False)
    category = Column(String)  # pensebete, agenda, reunion, retenue, appel, rdv_parent, rappel_cours, devoir
    created_at = Column(DateTime, default=datetime.utcnow)


class SeatAssignment(Base):
    """Seating plan assignment."""
    __tablename__ = "seat_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True)
    class_name = Column(String)
    row = Column(Integer)
    column = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="seat_assignment")


class Protocol(Base):
    """Protocol model (PAI, etc.)."""
    __tablename__ = "protocols"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    type = Column(String, nullable=False)  # PAI, PAP, PPS, etc.
    title = Column(String, nullable=False)
    description = Column(Text)
    actions = Column(JSON)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class AppConfig(Base):
    """Application configuration."""
    __tablename__ = "app_config"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(JSON)
    description = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LetterTemplate(Base):
    """Letter template model."""
    __tablename__ = "letter_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String)
    content = Column(Text, nullable=False)
    variables = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
