from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..dependencies import get_current_admin, get_current_user
from ..models import AppConfig, User
from ..schemas import ConfigPayload, ConfigRead

router = APIRouter(prefix="/config", tags=["config"])


@router.get("", response_model=ConfigRead)
async def get_config(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ConfigRead:
    config = await db.scalar(select(AppConfig).limit(1))
    if not config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuration absente")
    return ConfigRead.model_validate(config, from_attributes=True)


@router.put("", response_model=ConfigRead)
async def update_config(
    payload: ConfigPayload,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> ConfigRead:
    config = await db.scalar(select(AppConfig).limit(1))
    if not config:
        config = AppConfig()
        db.add(config)

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(config, key, value)

    await db.commit()
    await db.refresh(config)
    return ConfigRead.model_validate(config, from_attributes=True)
