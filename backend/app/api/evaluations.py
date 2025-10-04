from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Competence, Evaluation
from app.schemas import (
    CompetenceCreate,
    CompetenceResponse,
    EvaluationCreate,
    EvaluationResponse,
    CSVImportResponse
)
from app.services.csv_import import parse_competences_csv

router = APIRouter(prefix="/api/evaluations", tags=["Evaluations"])


@router.get("/competences", response_model=List[CompetenceResponse])
async def list_competences(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List all competences."""
    result = await db.execute(select(Competence))
    competences = result.scalars().all()
    return competences


@router.post("/competences", response_model=CompetenceResponse)
async def create_competence(
    competence: CompetenceCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new competence."""
    db_competence = Competence(**competence.model_dump())
    db.add(db_competence)
    await db.commit()
    await db.refresh(db_competence)
    return db_competence


@router.post("/competences/import", response_model=CSVImportResponse)
async def import_competences_csv(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Import competences from CSV file."""
    content = await file.read()
    content_str = content.decode("utf-8")
    
    competences_data, errors = parse_competences_csv(content_str)
    
    imported_count = 0
    for competence_data in competences_data:
        try:
            # Check if competence with this code already exists
            result = await db.execute(
                select(Competence).where(Competence.code == competence_data["code"])
            )
            existing = result.scalar_one_or_none()
            
            if not existing:
                competence = Competence(**competence_data)
                db.add(competence)
                imported_count += 1
        except Exception as e:
            errors.append(f"Failed to import competence: {str(e)}")
    
    await db.commit()
    
    return {
        "success": len(errors) == 0,
        "imported_count": imported_count,
        "errors": errors
    }


@router.get("/", response_model=List[EvaluationResponse])
async def list_evaluations(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    student_id: int = None
):
    """List evaluations."""
    query = select(Evaluation)
    
    if student_id:
        query = query.where(Evaluation.student_id == student_id)
    
    result = await db.execute(query)
    evaluations = result.scalars().all()
    return evaluations


@router.post("/", response_model=EvaluationResponse)
async def create_evaluation(
    evaluation: EvaluationCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new evaluation."""
    db_evaluation = Evaluation(**evaluation.model_dump())
    db.add(db_evaluation)
    await db.commit()
    await db.refresh(db_evaluation)
    return db_evaluation
