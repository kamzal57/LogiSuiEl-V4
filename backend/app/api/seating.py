from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models import User, Seat, Student
from app.schemas import SeatCreate, SeatUpdate, SeatResponse

router = APIRouter()

@router.get("/", response_model=List[SeatResponse])
async def get_seating_plan(
    class_name: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get seating plan, optionally filtered by class"""
    query = db.query(Seat)
    
    if class_name:
        query = query.filter(Seat.class_name == class_name)
    
    seats = query.all()
    return seats

@router.post("/", response_model=SeatResponse)
async def create_seat(
    seat: SeatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create or update a seat assignment"""
    # Check if student already has a seat
    existing_seat = db.query(Seat).filter(Seat.student_id == seat.student_id).first()
    
    if existing_seat:
        # Update existing seat
        existing_seat.class_name = seat.class_name
        existing_seat.row = seat.row
        existing_seat.column = seat.column
        db.commit()
        db.refresh(existing_seat)
        return existing_seat
    else:
        # Create new seat
        db_seat = Seat(**seat.model_dump())
        db.add(db_seat)
        db.commit()
        db.refresh(db_seat)
        return db_seat

@router.put("/{seat_id}", response_model=SeatResponse)
async def update_seat(
    seat_id: int,
    seat: SeatUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a seat assignment"""
    db_seat = db.query(Seat).filter(Seat.id == seat_id).first()
    
    if not db_seat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seat not found"
        )
    
    update_data = seat.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_seat, key, value)
    
    db.commit()
    db.refresh(db_seat)
    return db_seat

@router.delete("/{seat_id}")
async def delete_seat(
    seat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a seat assignment"""
    db_seat = db.query(Seat).filter(Seat.id == seat_id).first()
    
    if not db_seat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seat not found"
        )
    
    db.delete(db_seat)
    db.commit()
    return {"message": "Seat deleted successfully"}
