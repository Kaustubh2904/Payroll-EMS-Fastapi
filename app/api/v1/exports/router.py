from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import zipfile
import tempfile
from app.core.database import get_db
from app.api.dependencies import get_current_active_hr_admin
from app.services.export.export_service import generate_bank_export
from app.core.config import settings

router = APIRouter()

@router.get("/payroll/{id}/zip")
def download_payslips_zip(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_hr_admin)):
    from app.repositories.payroll_repo import PayrollRepository
    from app.services.pdf.pdf_service import generate_payslip_pdf
    repo = PayrollRepository(db)
    run = repo.get_run(id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(settings.EXPORTS_DIR, f"payslips_{id}.zip")
    os.makedirs(settings.EXPORTS_DIR, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for record in run.records:
            employee = record.employee
            if not employee:
                continue
            
            pdf_path = os.path.join(temp_dir, f"{employee.first_name}_{employee.last_name}_{record.id}.pdf")
            
            emp_data = {
                "name": f"{employee.first_name} {employee.last_name}",
                "code": employee.employee_code,
                "account": employee.bank_account_number or "N/A"
            }
            
            sal_data = {
                "month": run.month,
                "year": run.year,
                "gross": float(record.gross_salary),
                "deductions": float(record.total_deductions),
                "tax": float(record.tax_amount),
                "pt": float(record.professional_tax),
                "net": float(record.net_salary),
                "items": [{"name": i.component_name, "type": i.component_type, "amount": float(i.amount)} for i in record.items]
            }
            
            generate_payslip_pdf(record.id, emp_data, sal_data, pdf_path)
            zipf.write(pdf_path, os.path.basename(pdf_path))
            
    return FileResponse(zip_path, media_type="application/zip", filename=f"payslips_{id}.zip")

@router.get("/payroll/{id}/bank-file")
def download_bank_export(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_hr_admin)):
    try:
        file_path = generate_bank_export(db, id)
        return FileResponse(file_path, filename=os.path.basename(file_path), media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
