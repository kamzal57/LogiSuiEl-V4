from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date)
    class_name = Column(String, index=True)
    student_id = Column(String, unique=True, index=True)
    email = Column(String)
    phone = Column(String)
    address = Column(Text)
    parent_name = Column(String)
    parent_email = Column(String)
    parent_phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    evaluations = relationship("Evaluation", back_populates="student")
    incidents = relationship("Incident", back_populates="student")
    attendances = relationship("Attendance", back_populates="student")
    seat = relationship("Seat", back_populates="student", uselist=False)
    protocols = relationship("Protocol", back_populates="student")

class Competence(Base):
    __tablename__ = "competences"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)
    level = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    evaluations = relationship("Evaluation", back_populates="competence")

class Evaluation(Base):
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    competence_id = Column(Integer, ForeignKey("competences.id"), nullable=False)
    score = Column(Float)
    note = Column(String)
    evaluation_date = Column(DateTime, default=datetime.utcnow)
    period = Column(String)  # trimester or semester
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="evaluations")
    competence = relationship("Competence", back_populates="evaluations")

class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    type = Column(String, nullable=False)  # tardiness, absence, chatting, behavior, positive
    description = Column(Text)
    severity = Column(Integer)  # 1-5
    date = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)
    resolution_note = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    student = relationship("Student", back_populates="incidents")

class Attendance(Base):
    __tablename__ = "attendances"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String, nullable=False)  # present, absent, late, excused
    minutes_late = Column(Integer)
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="attendances")

class Seat(Base):
    __tablename__ = "seats"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True)
    class_name = Column(String, nullable=False)
    row = Column(Integer, nullable=False)
    column = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="seat")

class Protocol(Base):
    __tablename__ = "protocols"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    type = Column(String, nullable=False)  # PAI, PAP, etc.
    title = Column(String, nullable=False)
    description = Column(Text)
    actions = Column(Text)  # JSON string of actions to take
    start_date = Column(Date)
    end_date = Column(Date)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="protocols")

class TimetableEvent(Base):
    __tablename__ = "timetable_events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    class_name = Column(String)
    location = Column(String)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    day_of_week = Column(Integer)  # 0=Monday, 6=Sunday
    week_type = Column(String)  # A, B, or null for both
    is_recurring = Column(Boolean, default=False)
    color = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Reminder(Base):
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    type = Column(String, nullable=False)  # meeting, detention, parent_meeting, homework, personal
    due_date = Column(DateTime)
    is_completed = Column(Boolean, default=False)
    priority = Column(Integer, default=1)  # 1-5
    created_at = Column(DateTime, default=datetime.utcnow)

class UserPreferences(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    class_mode = Column(Boolean, default=False)
    language = Column(String, default="fr")
    theme = Column(String, default="light")
    widgets_enabled = Column(Text)  # JSON string of enabled widgets
    settings = Column(Text)  # JSON string of additional settings
    
    # Relationships
    user = relationship("User", back_populates="preferences")
