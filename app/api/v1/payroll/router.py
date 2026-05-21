from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.payroll import PayrollRunCreate, PayrollRunResponse, PayrollRunDetailsResponse
from app.services.payroll.payroll_service import PayrollService
from app.repositories.payroll_repo import PayrollRepository
from app.api.dependencies import get_current_active_hr_admin

router = APIRouter()

def get_payroll_service(db: Session = Depends(get_db)):
    return PayrollService(db)

def get_payroll_repo(db: Session = Depends(get_db)):
    return PayrollRepository(db)

@router.post("/run", response_model=PayrollRunResponse)
def generate_payroll(
    run_in: PayrollRunCreate,
    service: PayrollService = Depends(get_payroll_service),
    current_user = Depends(get_current_active_hr_admin)
):
    return service.generate_payroll(run_in.month, run_in.year, current_user.id)

@router.get("/history", response_model=List[PayrollRunResponse])
def get_payroll_history(
    repo: PayrollRepository = Depends(get_payroll_repo),
    current_user = Depends(get_current_active_hr_admin)
):
    return repo.get_history()

@router.get("/{id}", response_model=PayrollRunDetailsResponse)
def get_payroll_details(
    id: int,
    repo: PayrollRepository = Depends(get_payroll_repo),
    current_user = Depends(get_current_active_hr_admin)
):
    run = repo.get_run(id)
    if not run:
        raise HTTPException(status_code=404, detail="Payroll run not found")
    return run

@router.post("/{id}/approve", response_model=PayrollRunResponse)
def approve_payroll(
    id: int,
    service: PayrollService = Depends(get_payroll_service),
    current_user = Depends(get_current_active_hr_admin)
):
    return service.approve_payroll(id, current_user.id)

@router.post("/{id}/lock", response_model=PayrollRunResponse)
def lock_payroll(
    id: int,
    service: PayrollService = Depends(get_payroll_service),
    current_user = Depends(get_current_active_hr_admin)
):
    return service.lock_payroll(id, current_user.id)
