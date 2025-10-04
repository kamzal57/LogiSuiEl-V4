from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.security import get_current_user
from .. import models, schemas

router = APIRouter(prefix="/api/seating", tags=["seating"])


@router.get("/", response_model=List[schemas.Seat])
async def get_seating_plan(
    class_name: str = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get seating plan"""
    query = db.query(models.Seat).filter(models.Seat.teacher_id == current_user.id)
    if class_name:
        query = query.filter(models.Seat.class_name == class_name)
    seats = query.all()
    return seats


@router.post("/", response_model=schemas.Seat)
async def create_seat(
    seat: schemas.SeatCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create or update a seat"""
    # Check if seat already exists for this student
    existing = db.query(models.Seat).filter(
        models.Seat.student_id == seat.student_id,
        models.Seat.teacher_id == current_user.id
    ).first()
    
    if existing:
        # Update existing seat
        existing.row = seat.row
        existing.column = seat.column
        existing.class_name = seat.class_name
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new seat
        db_seat = models.Seat(**seat.dict(), teacher_id=current_user.id)
        db.add(db_seat)
        db.commit()
        db.refresh(db_seat)
        return db_seat


@router.delete("/{seat_id}")
async def delete_seat(
    seat_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a seat"""
    seat = db.query(models.Seat).filter(
        models.Seat.id == seat_id,
        models.Seat.teacher_id == current_user.id
    ).first()
    
    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")
    
    db.delete(seat)
    db.commit()
    return {"message": "Seat deleted successfully"}
