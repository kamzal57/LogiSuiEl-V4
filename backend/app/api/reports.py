from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import csv
import io

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Student, Evaluation, Incident

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/students/csv")
async def export_students_csv(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Export students to CSV."""
    result = await db.execute(select(Student))
    students = result.scalars().all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "ID", "First Name", "Last Name", "Class", 
        "Email", "Parent Contact", "Date of Birth"
    ])
    
    # Write data
    for student in students:
        writer.writerow([
            student.id,
            student.first_name,
            student.last_name,
            student.class_name or "",
            student.email or "",
            student.parent_contact or "",
            student.date_of_birth.strftime("%Y-%m-%d") if student.date_of_birth else ""
        ])
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=students.csv"}
    )


@router.get("/evaluations/csv")
async def export_evaluations_csv(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    student_id: int = None
):
    """Export evaluations to CSV."""
    query = select(Evaluation)
    if student_id:
        query = query.where(Evaluation.student_id == student_id)
    
    result = await db.execute(query)
    evaluations = result.scalars().all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "ID", "Student ID", "Type", "Value", "Grade", 
        "Comment", "Date", "Period"
    ])
    
    # Write data
    for evaluation in evaluations:
        writer.writerow([
            evaluation.id,
            evaluation.student_id,
            evaluation.type,
            evaluation.value or "",
            evaluation.grade or "",
            evaluation.comment or "",
            evaluation.date.strftime("%Y-%m-%d"),
            evaluation.period or ""
        ])
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=evaluations.csv"}
    )


@router.get("/incidents/csv")
async def export_incidents_csv(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Export incidents to CSV."""
    result = await db.execute(select(Incident))
    incidents = result.scalars().all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "ID", "Student ID", "Type", "Is Positive", 
        "Description", "Date", "Severity"
    ])
    
    # Write data
    for incident in incidents:
        writer.writerow([
            incident.id,
            incident.student_id,
            incident.type,
            incident.is_positive,
            incident.description or "",
            incident.date.strftime("%Y-%m-%d %H:%M:%S"),
            incident.severity
        ])
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=incidents.csv"}
    )
