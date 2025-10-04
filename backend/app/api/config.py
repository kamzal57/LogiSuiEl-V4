from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models import AppConfig
from app.schemas import AppConfigCreate, AppConfigResponse

router = APIRouter(prefix="/api/config", tags=["Configuration"])


@router.get("/", response_model=List[AppConfigResponse])
async def list_config(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List all configuration entries."""
    result = await db.execute(select(AppConfig))
    configs = result.scalars().all()
    return configs


@router.get("/{key}", response_model=AppConfigResponse)
async def get_config(
    key: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a specific configuration value."""
    result = await db.execute(select(AppConfig).where(AppConfig.key == key))
    config = result.scalar_one_or_none()
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    return config


@router.post("/", response_model=AppConfigResponse)
async def create_config(
    config: AppConfigCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("ADMIN"))
):
    """Create a new configuration entry."""
    # Check if key already exists
    result = await db.execute(select(AppConfig).where(AppConfig.key == config.key))
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(status_code=400, detail="Configuration key already exists")
    
    db_config = AppConfig(**config.model_dump())
    db.add(db_config)
    await db.commit()
    await db.refresh(db_config)
    return db_config


@router.put("/{key}", response_model=AppConfigResponse)
async def update_config(
    key: str,
    config: AppConfigCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("ADMIN"))
):
    """Update a configuration entry."""
    result = await db.execute(select(AppConfig).where(AppConfig.key == key))
    db_config = result.scalar_one_or_none()
    
    if not db_config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    for key, value in config.model_dump().items():
        setattr(db_config, key, value)
    
    await db.commit()
    await db.refresh(db_config)
    return db_config


@router.delete("/{key}")
async def delete_config(
    key: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("ADMIN"))
):
    """Delete a configuration entry."""
    result = await db.execute(select(AppConfig).where(AppConfig.key == key))
    config = result.scalar_one_or_none()
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    await db.delete(config)
    await db.commit()
    return {"success": True}
