from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.deduction import DeductionRuleCreate, DeductionRuleUpdate, DeductionRuleResponse
from app.repositories.deduction_repo import DeductionRepository
from app.api.dependencies import get_current_active_hr_admin

router = APIRouter()

def get_deduction_repo(db: Session = Depends(get_db)):
    return DeductionRepository(db)

@router.post("", response_model=DeductionRuleResponse)
def create_deduction_rule(
    rule_in: DeductionRuleCreate,
    repo: DeductionRepository = Depends(get_deduction_repo),
    current_user = Depends(get_current_active_hr_admin)
):
    return repo.create(rule_in)

@router.get("", response_model=List[DeductionRuleResponse])
def list_deductions(
    active_only: bool = False,
    repo: DeductionRepository = Depends(get_deduction_repo),
    current_user = Depends(get_current_active_hr_admin)
):
    return repo.get_all(active_only=active_only)

@router.put("/{id}", response_model=DeductionRuleResponse)
def update_deduction_rule(
    id: int,
    rule_in: DeductionRuleUpdate,
    repo: DeductionRepository = Depends(get_deduction_repo),
    current_user = Depends(get_current_active_hr_admin)
):
    rule = repo.get_by_id(id)
    if not rule:
        raise HTTPException(status_code=404, detail="Deduction rule not found")
    return repo.update(rule, rule_in)
