from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..dependencies import get_current_active_teacher, get_current_admin
from ..models import Protocol, Student, User
from ..schemas import ProtocolBase, ProtocolRead

router = APIRouter(prefix="/protocols", tags=["protocols"])


@router.get("", response_model=List[ProtocolRead])
async def list_protocols(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_active_teacher),
) -> List[ProtocolRead]:
    result = await db.execute(select(Protocol))
    protocols = result.scalars().all()
    return [ProtocolRead.model_validate(protocol, from_attributes=True) for protocol in protocols]


@router.post("", response_model=ProtocolRead, status_code=status.HTTP_201_CREATED)
async def create_protocol(
    payload: ProtocolBase,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> ProtocolRead:
    student = await db.scalar(select(Student).where(Student.id == payload.student_id))
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Élève introuvable")
    protocol = Protocol(**payload.model_dump())
    db.add(protocol)
    await db.commit()
    await db.refresh(protocol)
    return ProtocolRead.model_validate(protocol, from_attributes=True)


@router.put("/{protocol_id}", response_model=ProtocolRead)
async def update_protocol(
    protocol_id: int,
    payload: ProtocolBase,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> ProtocolRead:
    protocol = await db.scalar(select(Protocol).where(Protocol.id == protocol_id))
    if not protocol:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Protocole introuvable")
    for key, value in payload.model_dump().items():
        setattr(protocol, key, value)
    await db.commit()
    await db.refresh(protocol)
    return ProtocolRead.model_validate(protocol, from_attributes=True)
