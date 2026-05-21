from sqlalchemy.orm import Session
from app.models.payroll import PayrollRun, PayrollRecord, PayrollItem
from app.models.employee import Employee, EmployeeStatus
from typing import List, Optional

class PayrollRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_run(self, run_id: int) -> Optional[PayrollRun]:
        return self.db.query(PayrollRun).filter(PayrollRun.id == run_id).first()

    def get_run_by_month_year(self, month: int, year: int) -> Optional[PayrollRun]:
        return self.db.query(PayrollRun).filter(PayrollRun.month == month, PayrollRun.year == year).first()

    def get_history(self) -> List[PayrollRun]:
        return self.db.query(PayrollRun).order_by(PayrollRun.created_at.desc()).all()

    def get_active_employees(self) -> List[Employee]:
        return self.db.query(Employee).filter(Employee.status == EmployeeStatus.ACTIVE.value).all()

    def create_run(self, run: PayrollRun) -> PayrollRun:
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run

    def save_payroll_batch(self, run: PayrollRun, records: List[PayrollRecord], items: List[PayrollItem]):
        try:
            self.db.add(run)
            self.db.flush()
            
            for record in records:
                record.payroll_run_id = run.id
                self.db.add(record)
            
            self.db.flush()
            
            for index, item in enumerate(items):
                # Linking to specific record would be handled in service ideally
                self.db.add(item)

            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def update_run_status(self, run: PayrollRun, status: str, user_id: int = None) -> PayrollRun:
        run.status = status
        if status == "APPROVED":
            run.approved_by = user_id
            run.approved_at = func.now()
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run
