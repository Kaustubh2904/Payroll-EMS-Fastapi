from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.salary import SalaryStructureCreate, SalaryStructureUpdate, SalaryStructureResponse, StructureAssignmentCreate
from app.repositories.salary_repo import SalaryRepository
from app.api.dependencies import get_current_active_hr_admin

router = APIRouter()

def get_salary_repo(db: Session = Depends(get_db)):
    return SalaryRepository(db)

@router.post("", response_model=SalaryStructureResponse)
def create_salary_structure(
    structure_in: SalaryStructureCreate,
    repo: SalaryRepository = Depends(get_salary_repo),
    current_user = Depends(get_current_active_hr_admin)
):
    return repo.create_structure(structure_in)

@router.get("", response_model=List[SalaryStructureResponse])
def list_salary_structures(
    repo: SalaryRepository = Depends(get_salary_repo),
    current_user = Depends(get_current_active_hr_admin)
):
    return repo.list_structures()

@router.get("/{id}", response_model=SalaryStructureResponse)
def get_salary_structure(
    id: int,
    repo: SalaryRepository = Depends(get_salary_repo),
    current_user = Depends(get_current_active_hr_admin)
):
    structure = repo.get_structure(id)
    if not structure:
         raise HTTPException(status_code=404, detail="Salary Structure not found")
    return structure

@router.put("/{id}", response_model=SalaryStructureResponse)
def update_salary_structure(
    id: int,
    structure_in: SalaryStructureUpdate,
    repo: SalaryRepository = Depends(get_salary_repo),
    current_user = Depends(get_current_active_hr_admin)
):
    structure = repo.get_structure(id)
    if not structure:
         raise HTTPException(status_code=404, detail="Salary Structure not found")
    return repo.update_structure(structure, structure_in)

@router.post("/assign")
def assign_salary_structure(
    assignment_in: StructureAssignmentCreate,
    repo: SalaryRepository = Depends(get_salary_repo),
    current_user = Depends(get_current_active_hr_admin)
):
    return repo.assign_structure(assignment_in)
