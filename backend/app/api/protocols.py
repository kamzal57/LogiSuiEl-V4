from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models import User, Protocol
from app.schemas import ProtocolCreate, ProtocolUpdate, ProtocolResponse

router = APIRouter()

@router.get("/", response_model=List[ProtocolResponse])
async def get_protocols(
    student_id: int = None,
    is_active: bool = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get protocols, optionally filtered by student or active status"""
    query = db.query(Protocol)
    
    if student_id:
        query = query.filter(Protocol.student_id == student_id)
    if is_active is not None:
        query = query.filter(Protocol.is_active == is_active)
    
    protocols = query.all()
    return protocols

@router.get("/{protocol_id}", response_model=ProtocolResponse)
async def get_protocol(
    protocol_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific protocol by ID"""
    protocol = db.query(Protocol).filter(Protocol.id == protocol_id).first()
    
    if not protocol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Protocol not found"
        )
    
    return protocol

@router.post("/", response_model=ProtocolResponse)
async def create_protocol(
    protocol: ProtocolCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new protocol"""
    db_protocol = Protocol(**protocol.model_dump())
    db.add(db_protocol)
    db.commit()
    db.refresh(db_protocol)
    return db_protocol

@router.put("/{protocol_id}", response_model=ProtocolResponse)
async def update_protocol(
    protocol_id: int,
    protocol: ProtocolUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a protocol"""
    db_protocol = db.query(Protocol).filter(Protocol.id == protocol_id).first()
    
    if not db_protocol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Protocol not found"
        )
    
    update_data = protocol.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_protocol, key, value)
    
    db.commit()
    db.refresh(db_protocol)
    return db_protocol

@router.delete("/{protocol_id}")
async def delete_protocol(
    protocol_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    """Delete a protocol"""
    db_protocol = db.query(Protocol).filter(Protocol.id == protocol_id).first()
    
    if not db_protocol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Protocol not found"
        )
    
    db.delete(db_protocol)
    db.commit()
    return {"message": "Protocol deleted successfully"}
