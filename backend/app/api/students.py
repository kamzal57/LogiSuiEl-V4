from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..dependencies import get_current_active_teacher, get_current_admin
from ..models import Attendance, BehaviourLog, BehaviourCategory, Evaluation, Student, User
from ..schemas import (
    AttendanceCreate,
    AttendanceRead,
    BehaviourLogCreate,
    BehaviourLogRead,
    CSVImportSummary,
    EvaluationCreate,
    EvaluationRead,
    StudentCreate,
    StudentRead,
    StudentUpdate,
)
from ..services import csv_import

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=List[StudentRead])
async def list_students(
    class_name: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_teacher),
) -> List[StudentRead]:
    stmt = select(Student)
    # TODO: filtrer par classes assignées aux professeurs
    if class_name:
        stmt = stmt.where(Student.class_name == class_name)
    stmt = stmt.order_by(Student.last_name, Student.first_name)
    result = await db.execute(stmt)
    students = result.scalars().all()
    return [StudentRead.model_validate(student, from_attributes=True) for student in students]


@router.post("", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
async def create_student(
    payload: StudentCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> StudentRead:
    student = Student(**payload.model_dump())
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return StudentRead.model_validate(student, from_attributes=True)


@router.put("/{student_id}", response_model=StudentRead)
async def update_student(
    student_id: int,
    payload: StudentUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> StudentRead:
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Élève introuvable")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(student, key, value)
    await db.commit()
    await db.refresh(student)
    return StudentRead.model_validate(student, from_attributes=True)


@router.post("/import", response_model=CSVImportSummary)
async def import_students_csv(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> CSVImportSummary:
    summary = await csv_import.import_students(file, db)
    return summary


@router.post("/import-competences", response_model=CSVImportSummary)
async def import_competences_csv(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> CSVImportSummary:
    summary = await csv_import.import_competences(file, db)
    return summary


@router.post("/{student_id}/evaluations", response_model=EvaluationRead, status_code=status.HTTP_201_CREATED)
async def add_evaluation(
    student_id: int,
    payload: EvaluationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_teacher),
) -> EvaluationRead:
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Élève introuvable")

    evaluation = Evaluation(
        student_id=student_id,
        competence_id=payload.competence_id,
        score=payload.score,
        max_score=payload.max_score,
    appreciation=payload.appreciation,
    evaluated_at=payload.evaluated_at or datetime.utcnow(),
        evaluator_id=current_user.id,
        period=payload.period,
    )
    db.add(evaluation)
    await db.commit()
    await db.refresh(evaluation)
    return EvaluationRead.model_validate(evaluation, from_attributes=True)


@router.post("/{student_id}/behaviours", response_model=BehaviourLogRead, status_code=status.HTTP_201_CREATED)
async def add_behaviour_log(
    student_id: int,
    payload: BehaviourLogCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_teacher),
) -> BehaviourLogRead:
    if payload.category != BehaviourCategory.POSITIVE and not payload.details:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Une note est requise")

    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Élève introuvable")

    log = BehaviourLog(
        student_id=student_id,
        teacher_id=current_user.id,
        category=payload.category,
        details=payload.details,
        is_positive=payload.is_positive,
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return BehaviourLogRead.model_validate(log, from_attributes=True)


@router.post("/{student_id}/attendance", response_model=AttendanceRead, status_code=status.HTTP_201_CREATED)
async def add_attendance(
    student_id: int,
    payload: AttendanceCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_active_teacher),
) -> AttendanceRead:
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Élève introuvable")

    attendance = Attendance(
        student_id=student_id,
        status=payload.status,
        comment=payload.comment,
        occurred_at=payload.occurred_at or datetime.utcnow(),
    )
    db.add(attendance)
    await db.commit()
    await db.refresh(attendance)
    return AttendanceRead.model_validate(attendance, from_attributes=True)
