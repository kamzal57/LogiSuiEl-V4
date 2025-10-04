from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Protocol
from app.schemas import ProtocolCreate, ProtocolResponse

router = APIRouter(prefix="/api/protocols", tags=["Protocols"])


@router.get("/", response_model=List[ProtocolResponse])
async def list_protocols(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    protocol_type: str = None
):
    """List protocols."""
    query = select(Protocol)
    
    if protocol_type:
        query = query.where(Protocol.type == protocol_type)
    
    result = await db.execute(query)
    protocols = result.scalars().all()
    return protocols


@router.post("/", response_model=ProtocolResponse)
async def create_protocol(
    protocol: ProtocolCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new protocol."""
    db_protocol = Protocol(**protocol.model_dump())
    db.add(db_protocol)
    await db.commit()
    await db.refresh(db_protocol)
    return db_protocol


@router.get("/{protocol_id}", response_model=ProtocolResponse)
async def get_protocol(
    protocol_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a specific protocol."""
    result = await db.execute(select(Protocol).where(Protocol.id == protocol_id))
    protocol = result.scalar_one_or_none()
    
    if not protocol:
        raise HTTPException(status_code=404, detail="Protocol not found")
    
    return protocol


@router.delete("/{protocol_id}")
async def delete_protocol(
    protocol_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a protocol."""
    result = await db.execute(select(Protocol).where(Protocol.id == protocol_id))
    protocol = result.scalar_one_or_none()
    
    if not protocol:
        raise HTTPException(status_code=404, detail="Protocol not found")
    
    await db.delete(protocol)
    await db.commit()
    return {"success": True}
