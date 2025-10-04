from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from .core.database import Base


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # ADMIN or TEACHER
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Preferences
    preferences = relationship("UserPreferences", back_populates="user", uselist=False)


class UserPreferences(Base):
    """User preferences and settings"""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    language = Column(String, default="fr")
    class_mode = Column(Boolean, default=False)  # Mode Classe
    theme = Column(String, default="light")
    
    user = relationship("User", back_populates="preferences")


class Student(Base):
    """Student model"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date)
    class_name = Column(String)
    student_id = Column(String, unique=True, index=True)
    email = Column(String)
    phone = Column(String)
    address = Column(Text)
    parent_name = Column(String)
    parent_email = Column(String)
    parent_phone = Column(String)
    medical_info = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    evaluations = relationship("Evaluation", back_populates="student")
    incidents = relationship("Incident", back_populates="student")
    attendances = relationship("Attendance", back_populates="student")
    seat = relationship("Seat", back_populates="student", uselist=False)
    protocols = relationship("Protocol", back_populates="student")


class Competence(Base):
    """Competence/Skill model"""
    __tablename__ = "competences"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)
    level = Column(String)
    
    # Relationships
    evaluations = relationship("Evaluation", back_populates="competence")


class Evaluation(Base):
    """Evaluation model for grades and competences"""
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    competence_id = Column(Integer, ForeignKey("competences.id"), nullable=True)
    type = Column(String)  # NOTE, COMPETENCE, BILAN
    value = Column(Float)  # Note or competence level
    max_value = Column(Float, default=20.0)
    comment = Column(Text)
    date = Column(DateTime, default=datetime.utcnow)
    period = Column(String)  # Trimester
    subject = Column(String)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    student = relationship("Student", back_populates="evaluations")
    competence = relationship("Competence", back_populates="evaluations")


class Incident(Base):
    """Incident model for behavior tracking"""
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    type = Column(String)  # RETARD, ABSENCE, BAVARDAGE, COMPORTEMENT, OUBLI, MANQUE_TRAVAIL, PARTICIPATION_POSITIVE
    description = Column(Text)
    date = Column(DateTime, default=datetime.utcnow)
    is_positive = Column(Boolean, default=False)
    points = Column(Integer, default=0)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    student = relationship("Student", back_populates="incidents")


class Attendance(Base):
    """Attendance tracking"""
    __tablename__ = "attendances"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(DateTime, nullable=False)
    status = Column(String)  # PRESENT, ABSENT, RETARD, EXCUSE
    reason = Column(Text)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    student = relationship("Student", back_populates="attendances")


class TimetableEvent(Base):
    """Timetable/Schedule event"""
    __tablename__ = "timetable_events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String)
    class_name = Column(String)
    subject = Column(String)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    is_recurring = Column(Boolean, default=False)
    recurrence_rule = Column(String)


class Reminder(Base):
    """Reminder/Note model"""
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    type = Column(String)  # NOTE, REUNION, APPEL, RDV_PARENT, RAPPEL_COURS, RAPPEL_DEVOIR
    due_date = Column(DateTime)
    is_completed = Column(Boolean, default=False)
    priority = Column(String, default="NORMAL")  # LOW, NORMAL, HIGH
    teacher_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)


class Seat(Base):
    """Seating plan position"""
    __tablename__ = "seats"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True)
    class_name = Column(String)
    row = Column(Integer)
    column = Column(Integer)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    student = relationship("Student", back_populates="seat")


class Protocol(Base):
    """Protocol model (PAI, etc.)"""
    __tablename__ = "protocols"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    type = Column(String)  # PAI, PAP, PPS, etc.
    title = Column(String, nullable=False)
    description = Column(Text)
    actions = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="protocols")


class LetterTemplate(Base):
    """Letter template model"""
    __tablename__ = "letter_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    type = Column(String)  # CONVOCATION, INFORMATION, FELICITATIONS, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    teacher_id = Column(Integer, ForeignKey("users.id"))


class SchoolConfig(Base):
    """School configuration"""
    __tablename__ = "school_config"
    
    id = Column(Integer, primary_key=True, index=True)
    school_name = Column(String)
    school_address = Column(Text)
    school_phone = Column(String)
    school_email = Column(String)
    academic_year = Column(String)
    periods = Column(Text)  # JSON string for periods/trimesters
    timetable_config = Column(Text)  # JSON string for timetable configuration
    holidays = Column(Text)  # JSON string for holidays
