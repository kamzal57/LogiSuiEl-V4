from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models import User, Competence
from app.schemas import CompetenceCreate, CompetenceUpdate, CompetenceResponse
from app.services.csv_import import parse_competences_csv

router = APIRouter()

@router.get("/", response_model=List[CompetenceResponse])
async def get_competences(
    category: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all competences, optionally filtered by category"""
    query = db.query(Competence)
    
    if category:
        query = query.filter(Competence.category == category)
    
    competences = query.all()
    return competences

@router.get("/{competence_id}", response_model=CompetenceResponse)
async def get_competence(
    competence_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific competence by ID"""
    competence = db.query(Competence).filter(Competence.id == competence_id).first()
    
    if not competence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Competence not found"
        )
    
    return competence

@router.post("/", response_model=CompetenceResponse)
async def create_competence(
    competence: CompetenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    """Create a new competence"""
    # Check if code already exists
    existing = db.query(Competence).filter(Competence.code == competence.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Competence with this code already exists"
        )
    
    db_competence = Competence(**competence.model_dump())
    db.add(db_competence)
    db.commit()
    db.refresh(db_competence)
    return db_competence

@router.put("/{competence_id}", response_model=CompetenceResponse)
async def update_competence(
    competence_id: int,
    competence: CompetenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    """Update a competence"""
    db_competence = db.query(Competence).filter(Competence.id == competence_id).first()
    
    if not db_competence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Competence not found"
        )
    
    update_data = competence.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_competence, key, value)
    
    db.commit()
    db.refresh(db_competence)
    return db_competence

@router.delete("/{competence_id}")
async def delete_competence(
    competence_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    """Delete a competence"""
    db_competence = db.query(Competence).filter(Competence.id == competence_id).first()
    
    if not db_competence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Competence not found"
        )
    
    db.delete(db_competence)
    db.commit()
    return {"message": "Competence deleted successfully"}

@router.post("/import")
async def import_competences(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    """Import competences from CSV file"""
    try:
        competences_data = await parse_competences_csv(file)
        
        imported_count = 0
        for competence_data in competences_data:
            # Check if competence already exists by code
            existing_competence = db.query(Competence).filter(
                Competence.code == competence_data['code']
            ).first()
            
            if existing_competence:
                # Update existing competence
                for key, value in competence_data.items():
                    if value:  # Only update non-empty values
                        setattr(existing_competence, key, value)
            else:
                # Create new competence
                db_competence = Competence(**competence_data)
                db.add(db_competence)
            
            imported_count += 1
        
        db.commit()
        
        return {
            "message": f"Successfully imported {imported_count} competences",
            "count": imported_count
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to import competences: {str(e)}"
        )
