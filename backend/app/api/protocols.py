from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.security import get_current_user
from .. import models, schemas

router = APIRouter(prefix="/api/protocols", tags=["protocols"])


@router.get("/", response_model=List[schemas.Protocol])
async def get_protocols(
    is_active: bool = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get protocols (PAI, PAP, PPS, etc.)"""
    query = db.query(models.Protocol)
    if is_active is not None:
        query = query.filter(models.Protocol.is_active == is_active)
    protocols = query.all()
    return protocols


@router.post("/", response_model=schemas.Protocol)
async def create_protocol(
    protocol: schemas.ProtocolCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new protocol"""
    db_protocol = models.Protocol(**protocol.dict())
    db.add(db_protocol)
    db.commit()
    db.refresh(db_protocol)
    return db_protocol


@router.put("/{protocol_id}", response_model=schemas.Protocol)
async def update_protocol(
    protocol_id: int,
    protocol: schemas.ProtocolCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a protocol"""
    db_protocol = db.query(models.Protocol).filter(models.Protocol.id == protocol_id).first()
    if not db_protocol:
        raise HTTPException(status_code=404, detail="Protocol not found")
    
    for key, value in protocol.dict().items():
        setattr(db_protocol, key, value)
    
    db.commit()
    db.refresh(db_protocol)
    return db_protocol


@router.delete("/{protocol_id}")
async def delete_protocol(
    protocol_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a protocol"""
    db_protocol = db.query(models.Protocol).filter(models.Protocol.id == protocol_id).first()
    if not db_protocol:
        raise HTTPException(status_code=404, detail="Protocol not found")
    
    db.delete(db_protocol)
    db.commit()
    return {"message": "Protocol deleted successfully"}
