from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.security import get_current_user
from .. import models, schemas

router = APIRouter(prefix="/api/competences", tags=["competences"])


@router.get("/", response_model=List[schemas.Competence])
async def get_competences(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of competences"""
    query = db.query(models.Competence)
    if category:
        query = query.filter(models.Competence.category == category)
    competences = query.offset(skip).limit(limit).all()
    return competences


@router.post("/", response_model=schemas.Competence)
async def create_competence(
    competence: schemas.CompetenceCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new competence"""
    db_competence = models.Competence(**competence.dict())
    db.add(db_competence)
    db.commit()
    db.refresh(db_competence)
    return db_competence


@router.post("/import", response_model=schemas.ImportResponse)
async def import_competences(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Import competences from CSV file"""
    from ..services.csv_import import import_competences_from_csv
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    contents = await file.read()
    result = import_competences_from_csv(contents.decode('utf-8'), db)
    return result
