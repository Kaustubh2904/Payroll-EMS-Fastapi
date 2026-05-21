from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.tax import TaxSlabCreate, TaxSlabUpdate, TaxSlabResponse
from app.repositories.tax_repo import TaxRepository
from app.api.dependencies import get_current_active_hr_admin

router = APIRouter()

def get_tax_repo(db: Session = Depends(get_db)):
    return TaxRepository(db)

@router.post("-slabs", response_model=TaxSlabResponse)
def create_tax_slab(
    slab_in: TaxSlabCreate,
    repo: TaxRepository = Depends(get_tax_repo),
    current_user = Depends(get_current_active_hr_admin)
):
    return repo.create_slab(slab_in)

@router.get("-slabs", response_model=List[TaxSlabResponse])
def list_tax_slabs(
    repo: TaxRepository = Depends(get_tax_repo),
    current_user = Depends(get_current_active_hr_admin)
):
    return repo.list_slabs()

@router.put("-slabs/{id}", response_model=TaxSlabResponse)
def update_tax_slab(
    id: int,
    slab_in: TaxSlabUpdate,
    repo: TaxRepository = Depends(get_tax_repo),
    current_user = Depends(get_current_active_hr_admin)
):
    slab = repo.get_slab(id)
    if not slab:
        raise HTTPException(status_code=404, detail="Tax Slab not found")
    return repo.update_slab(slab, slab_in)
