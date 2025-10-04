from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Student, Incident, Evaluation
from app.schemas import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    IncidentCreate,
    IncidentResponse,
    CSVImportResponse
)
from app.services.csv_import import parse_students_csv

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.get("/", response_model=List[StudentResponse])
async def list_students(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """List all students."""
    result = await db.execute(select(Student).offset(skip).limit(limit))
    students = result.scalars().all()
    return students


@router.post("/", response_model=StudentResponse)
async def create_student(
    student: StudentCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new student."""
    db_student = Student(**student.model_dump())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a specific student."""
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student_update: StudentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update a student."""
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for key, value in student_update.model_dump(exclude_unset=True).items():
        setattr(student, key, value)
    
    await db.commit()
    await db.refresh(student)
    return student


@router.delete("/{student_id}")
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a student."""
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    await db.delete(student)
    await db.commit()
    return {"success": True}


@router.post("/import", response_model=CSVImportResponse)
async def import_students_csv(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Import students from CSV file."""
    content = await file.read()
    content_str = content.decode("utf-8")
    
    students_data, errors = parse_students_csv(content_str)
    
    imported_count = 0
    for student_data in students_data:
        try:
            student = Student(**student_data)
            db.add(student)
            imported_count += 1
        except Exception as e:
            errors.append(f"Failed to import student: {str(e)}")
    
    await db.commit()
    
    return {
        "success": len(errors) == 0,
        "imported_count": imported_count,
        "errors": errors
    }


@router.post("/{student_id}/incidents", response_model=IncidentResponse)
async def create_student_incident(
    student_id: int,
    incident: IncidentCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create an incident for a student."""
    # Verify student exists
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db_incident = Incident(**incident.model_dump())
    db.add(db_incident)
    await db.commit()
    await db.refresh(db_incident)
    return db_incident


@router.get("/{student_id}/incidents", response_model=List[IncidentResponse])
async def get_student_incidents(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all incidents for a student."""
    result = await db.execute(
        select(Incident).where(Incident.student_id == student_id)
    )
    incidents = result.scalars().all()
    return incidents
