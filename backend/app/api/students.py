from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.security import get_current_user
from .. import models, schemas

router = APIRouter(prefix="/api/students", tags=["students"])


@router.get("/", response_model=List[schemas.Student])
async def get_students(
    skip: int = 0,
    limit: int = 100,
    class_name: str = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of students"""
    query = db.query(models.Student)
    if class_name:
        query = query.filter(models.Student.class_name == class_name)
    students = query.offset(skip).limit(limit).all()
    return students


@router.get("/{student_id}", response_model=schemas.Student)
async def get_student(
    student_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific student"""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/", response_model=schemas.Student)
async def create_student(
    student: schemas.StudentCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new student"""
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.put("/{student_id}", response_model=schemas.Student)
async def update_student(
    student_id: int,
    student: schemas.StudentCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a student"""
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for key, value in student.dict().items():
        setattr(db_student, key, value)
    
    db.commit()
    db.refresh(db_student)
    return db_student


@router.delete("/{student_id}")
async def delete_student(
    student_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a student"""
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}


@router.post("/import", response_model=schemas.ImportResponse)
async def import_students(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Import students from CSV file"""
    from ..services.csv_import import import_students_from_csv
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    contents = await file.read()
    result = import_students_from_csv(contents.decode('utf-8'), db)
    return result


@router.post("/{student_id}/incidents", response_model=schemas.Incident)
async def add_incident(
    student_id: int,
    incident: schemas.IncidentCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add an incident for a student"""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db_incident = models.Incident(**incident.dict(), teacher_id=current_user.id)
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident


@router.post("/{student_id}/evaluations", response_model=schemas.Evaluation)
async def add_evaluation(
    student_id: int,
    evaluation: schemas.EvaluationCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add an evaluation for a student"""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db_evaluation = models.Evaluation(**evaluation.dict(), teacher_id=current_user.id)
    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation
