from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Evaluation, Incident, Attendance
from app.schemas import (
    EvaluationCreate, EvaluationUpdate, EvaluationResponse,
    IncidentCreate, IncidentUpdate, IncidentResponse,
    AttendanceCreate, AttendanceUpdate, AttendanceResponse
)

router = APIRouter()

# Evaluations
@router.get("/evaluations", response_model=List[EvaluationResponse])
async def get_evaluations(
    student_id: int = None,
    period: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get evaluations, optionally filtered by student or period"""
    query = db.query(Evaluation)
    
    if student_id:
        query = query.filter(Evaluation.student_id == student_id)
    if period:
        query = query.filter(Evaluation.period == period)
    
    evaluations = query.all()
    return evaluations

@router.post("/evaluations", response_model=EvaluationResponse)
async def create_evaluation(
    evaluation: EvaluationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new evaluation"""
    db_evaluation = Evaluation(**evaluation.model_dump())
    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation

@router.put("/evaluations/{evaluation_id}", response_model=EvaluationResponse)
async def update_evaluation(
    evaluation_id: int,
    evaluation: EvaluationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an evaluation"""
    db_evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    
    if not db_evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluation not found"
        )
    
    update_data = evaluation.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_evaluation, key, value)
    
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation

# Incidents
@router.get("/incidents", response_model=List[IncidentResponse])
async def get_incidents(
    student_id: int = None,
    type: str = None,
    resolved: bool = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get incidents, optionally filtered"""
    query = db.query(Incident)
    
    if student_id:
        query = query.filter(Incident.student_id == student_id)
    if type:
        query = query.filter(Incident.type == type)
    if resolved is not None:
        query = query.filter(Incident.resolved == resolved)
    
    incidents = query.order_by(Incident.date.desc()).all()
    return incidents

@router.post("/incidents", response_model=IncidentResponse)
async def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new incident"""
    db_incident = Incident(**incident.model_dump())
    db_incident.created_by = current_user.id
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@router.put("/incidents/{incident_id}", response_model=IncidentResponse)
async def update_incident(
    incident_id: int,
    incident: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an incident"""
    db_incident = db.query(Incident).filter(Incident.id == incident_id).first()
    
    if not db_incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found"
        )
    
    update_data = incident.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_incident, key, value)
    
    db.commit()
    db.refresh(db_incident)
    return db_incident

# Attendance
@router.get("/attendance", response_model=List[AttendanceResponse])
async def get_attendance(
    student_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get attendance records"""
    query = db.query(Attendance)
    
    if student_id:
        query = query.filter(Attendance.student_id == student_id)
    
    attendance = query.order_by(Attendance.date.desc()).all()
    return attendance

@router.post("/attendance", response_model=AttendanceResponse)
async def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new attendance record"""
    db_attendance = Attendance(**attendance.model_dump())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.put("/attendance/{attendance_id}", response_model=AttendanceResponse)
async def update_attendance(
    attendance_id: int,
    attendance: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an attendance record"""
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    
    if not db_attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )
    
    update_data = attendance.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_attendance, key, value)
    
    db.commit()
    db.refresh(db_attendance)
    return db_attendance
