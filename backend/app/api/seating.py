from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..dependencies import get_current_active_teacher
from ..models import SeatingPosition, Student, User
from ..schemas import SeatingPositionBase, SeatingPositionRead

router = APIRouter(prefix="/seating-plan", tags=["seating"])


@router.get("", response_model=List[SeatingPositionRead])
async def get_seating_plan(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_active_teacher),
) -> List[SeatingPositionRead]:
    result = await db.execute(select(SeatingPosition))
    positions = result.scalars().all()
    return [SeatingPositionRead.model_validate(pos, from_attributes=True) for pos in positions]


@router.put("", response_model=List[SeatingPositionRead])
async def update_seating_plan(
    payload: List[SeatingPositionBase],
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_active_teacher),
) -> List[SeatingPositionRead]:
    # validate students
    student_ids = {item.student_id for item in payload}
    existing_students = await db.execute(select(Student.id).where(Student.id.in_(student_ids)))
    existing_ids = {sid for (sid,) in existing_students.all()}
    missing = student_ids - existing_ids
    if missing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Élèves manquants: {missing}")

    await db.execute(delete(SeatingPosition))

    new_positions: list[SeatingPosition] = []
    for item in payload:
        position = SeatingPosition(**item.model_dump())
        db.add(position)
        new_positions.append(position)
    await db.commit()

    return [SeatingPositionRead.model_validate(pos, from_attributes=True) for pos in new_positions]
