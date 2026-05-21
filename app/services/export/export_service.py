import pandas as pd
import os
from sqlalchemy.orm import Session
from app.models.payroll import PayrollRun, PayrollRecord
from app.core.config import settings

def generate_bank_export(db: Session, payroll_run_id: int) -> str:
    from app.repositories.payroll_repo import PayrollRepository
    repo = PayrollRepository(db)
    
    run = repo.get_run(payroll_run_id)
    if not run:
        raise ValueError("Run not found")
        
    data = []
    
    # Assuming relationship loading 
    for record in run.records:
        employee = record.employee
        if employee:
            data.append({
                "Employee Name": f"{employee.first_name} {employee.last_name}",
                "Account Number": employee.bank_account_number,
                "IFSC Code": employee.ifsc_code,
                "Net Salary": float(record.net_salary)
            })
            
    df = pd.DataFrame(data)
    
    export_dir = settings.EXPORTS_DIR
    os.makedirs(export_dir, exist_ok=True)
    
    file_path = os.path.join(export_dir, f"bank_export_run_{payroll_run_id}.xlsx")
    df.to_excel(file_path, index=False)
    
    return file_path
