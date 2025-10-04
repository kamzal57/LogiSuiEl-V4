from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import SeatAssignment, Student
from app.schemas import SeatAssignmentCreate, SeatAssignmentResponse

router = APIRouter(prefix="/api/seating", tags=["Seating Plan"])


@router.get("/", response_model=List[SeatAssignmentResponse])
async def list_seat_assignments(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    class_name: str = None
):
    """List seat assignments."""
    query = select(SeatAssignment)
    
    if class_name:
        query = query.where(SeatAssignment.class_name == class_name)
    
    result = await db.execute(query)
    seats = result.scalars().all()
    return seats


@router.post("/", response_model=SeatAssignmentResponse)
async def create_seat_assignment(
    seat: SeatAssignmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create or update a seat assignment."""
    # Check if student exists
    result = await db.execute(select(Student).where(Student.id == seat.student_id))
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if assignment already exists for this student
    result = await db.execute(
        select(SeatAssignment).where(SeatAssignment.student_id == seat.student_id)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        # Update existing assignment
        for key, value in seat.model_dump().items():
            setattr(existing, key, value)
        await db.commit()
        await db.refresh(existing)
        return existing
    else:
        # Create new assignment
        db_seat = SeatAssignment(**seat.model_dump())
        db.add(db_seat)
        await db.commit()
        await db.refresh(db_seat)
        return db_seat


@router.delete("/{seat_id}")
async def delete_seat_assignment(
    seat_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a seat assignment."""
    result = await db.execute(
        select(SeatAssignment).where(SeatAssignment.id == seat_id)
    )
    seat = result.scalar_one_or_none()
    
    if not seat:
        raise HTTPException(status_code=404, detail="Seat assignment not found")
    
    await db.delete(seat)
    await db.commit()
    return {"success": True}
