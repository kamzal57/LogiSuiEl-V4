import csv
from io import StringIO
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..dependencies import get_current_admin
from ..models import BehaviourLog, Student, User
from ..schemas import ReportResponse

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{report_type}", response_model=ReportResponse)
async def export_report(
    report_type: Literal["students", "behaviours"],
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> ReportResponse:
    if report_type == "students":
        return await _export_students(db)
    if report_type == "behaviours":
        return await _export_behaviours(db)
    raise HTTPException(status_code=404, detail="Type de rapport inconnu")


async def _export_students(db: AsyncSession) -> ReportResponse:
    result = await db.execute(select(Student))
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "first_name", "last_name", "class", "email"])
    for student in result.scalars().all():
        writer.writerow([student.id, student.first_name, student.last_name, student.class_name, student.email])
    return ReportResponse(
        filename="students.csv",
        content_type="text/csv",
        data=output.getvalue(),
    )


async def _export_behaviours(db: AsyncSession) -> ReportResponse:
    result = await db.execute(select(BehaviourLog))
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["student_id", "category", "details", "logged_at"])
    for log in result.scalars().all():
        writer.writerow([log.student_id, log.category.value, log.details or "", log.logged_at.isoformat()])
    return ReportResponse(
        filename="behaviours.csv",
        content_type="text/csv",
        data=output.getvalue(),
    )
