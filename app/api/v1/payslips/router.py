from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
from app.core.database import get_db
from app.api.dependencies import get_current_active_hr_admin
from app.models.payroll import Payslip, PayrollRecord
from app.schemas.payslip import PayslipResponse

router = APIRouter()

@router.get("/{employee_id}", response_model=List[PayslipResponse])
def get_employee_payslips(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_hr_admin)
):
    payslips = db.query(Payslip).join(PayrollRecord).filter(PayrollRecord.employee_id == employee_id).all()
    return payslips

@router.get("/download/{id}")
def download_payslip_pdf(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_hr_admin)
):
    payslip = db.query(Payslip).filter(Payslip.id == id).first()
    if not payslip:
        raise HTTPException(status_code=404, detail="Payslip not found")
        
    if not os.path.exists(payslip.file_url):
        raise HTTPException(status_code=404, detail="Payslip file not found on server")
        
    return FileResponse(payslip.file_url, media_type="application/pdf", filename=os.path.basename(payslip.file_url))
