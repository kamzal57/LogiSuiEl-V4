from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models import User, Student
from app.schemas import StudentCreate, StudentUpdate, StudentResponse
from app.services.csv_import import parse_students_csv

router = APIRouter()

@router.get("/", response_model=List[StudentResponse])
async def get_students(
    class_name: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all students, optionally filtered by class"""
    query = db.query(Student)
    
    if class_name:
        query = query.filter(Student.class_name == class_name)
    
    students = query.all()
    return students

@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific student by ID"""
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return student

@router.post("/", response_model=StudentResponse)
async def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    """Create a new student"""
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    """Update a student"""
    db_student = db.query(Student).filter(Student.id == student_id).first()
    
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    update_data = student.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)
    
    db.commit()
    db.refresh(db_student)
    return db_student

@router.delete("/{student_id}")
async def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    """Delete a student"""
    db_student = db.query(Student).filter(Student.id == student_id).first()
    
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}

@router.post("/import")
async def import_students(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    """Import students from CSV file"""
    try:
        students_data = await parse_students_csv(file)
        
        imported_count = 0
        for student_data in students_data:
            # Check if student already exists by student_id
            existing_student = None
            if student_data.get('student_id'):
                existing_student = db.query(Student).filter(
                    Student.student_id == student_data['student_id']
                ).first()
            
            if existing_student:
                # Update existing student
                for key, value in student_data.items():
                    if value:  # Only update non-empty values
                        setattr(existing_student, key, value)
            else:
                # Create new student
                db_student = Student(**student_data)
                db.add(db_student)
            
            imported_count += 1
        
        db.commit()
        
        return {
            "message": f"Successfully imported {imported_count} students",
            "count": imported_count
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to import students: {str(e)}"
        )
