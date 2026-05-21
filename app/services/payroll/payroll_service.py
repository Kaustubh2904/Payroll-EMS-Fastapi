from decimal import Decimal
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
import logging

from app.models.payroll import PayrollRun, PayrollRecord, PayrollItem
from app.repositories.payroll_repo import PayrollRepository
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.salary_repo import SalaryRepository
from app.repositories.deduction_repo import DeductionRepository
from app.repositories.tax_repo import TaxRepository
from app.schemas.payroll import PayrollRunCreate

logger = logging.getLogger(__name__)

class PayrollService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PayrollRepository(db)
        self.emp_repo = EmployeeRepository(db)
        self.sal_repo = SalaryRepository(db)
        self.ded_repo = DeductionRepository(db)
        self.tax_repo = TaxRepository(db)

    def generate_payroll(self, month: int, year: int, user_id: int) -> PayrollRun:
        existing_run = self.repo.get_run_by_month_year(month, year)
        if existing_run:
            raise HTTPException(status_code=400, detail="Payroll for this month already exists")

        employees = self.repo.get_active_employees()
        if not employees:
            raise HTTPException(status_code=400, detail="No active employees found")

        deduction_rules = self.ded_repo.get_all(active_only=True)
        pf_settings = self.tax_repo.get_active_pf_setting()

        run = PayrollRun(
            month=month,
            year=year,
            status="GENERATED",
            processed_by=user_id,
        )

        records = []
        
        try:
            for emp in employees:
                assignment = self.sal_repo.get_active_assignment(emp.id)
                if not assignment:
                    logger.warning(f"Employee {emp.id} has no active salary structure. Skipping.")
                    continue

                structure = self.sal_repo.get_structure(assignment.salary_structure_id)
                if not structure:
                    continue

                gross_salary = Decimal("0.00")
                total_deductions = Decimal("0.00")
                pf_amount = Decimal("0.00")
                tax_amount = Decimal("0.00")
                professional_tax = Decimal("0.00")

                items = []

                # Calculate components
                basic_amount_for_pf = Decimal("0.00")
                
                for comp in structure.components:
                    val = Decimal(str(comp.amount))
                    if comp.component_type == "earning":
                        gross_salary += val
                        if comp.is_pf_applicable:
                            basic_amount_for_pf += val
                    
                    items.append(PayrollItem(
                        component_name=comp.component_name,
                        component_type=comp.component_type,
                        amount=val
                    ))

                # PF Calculation
                if pf_settings and pf_settings.enabled and basic_amount_for_pf > 0:
                    base_for_pf = min(basic_amount_for_pf, Decimal(str(pf_settings.wage_ceiling)))
                    pf_amount = base_for_pf * (Decimal(str(pf_settings.employee_contribution)) / Decimal("100"))
                    total_deductions += pf_amount
                    items.append(PayrollItem(
                        component_name="Employee PF",
                        component_type="deduction",
                        amount=pf_amount
                    ))

                # Apply Deductions
                for rule in deduction_rules:
                    deduct = Decimal("0.00")
                    if rule.calculation_type == "fixed":
                        deduct = Decimal(str(rule.fixed_amount))
                    elif rule.calculation_type == "percentage":
                        deduct = gross_salary * (Decimal(str(rule.percentage)) / Decimal("100"))
                        if rule.max_limit and deduct > Decimal(str(rule.max_limit)):
                           deduct = Decimal(str(rule.max_limit))
                    
                    total_deductions += deduct
                    items.append(PayrollItem(
                        component_name=rule.name,
                        component_type="deduction",
                        amount=deduct
                    ))
                
                # Tax calculation based on slabs
                slabs = self.tax_repo.list_slabs(regime_type="NEW")
                annual_income = (gross_salary - total_deductions) * 12
                
                annual_tax = Decimal("0.00")
                for slab in slabs:
                    slab_min = Decimal(str(slab.min_income))
                    slab_max = Decimal(str(slab.max_income)) if slab.max_income is not None else None
                    
                    if annual_income > slab_min:
                        if slab_max is not None:
                            taxable_in_slab = min(annual_income, slab_max) - slab_min
                        else:
                            taxable_in_slab = annual_income - slab_min
                            
                        if taxable_in_slab > 0:
                            annual_tax += taxable_in_slab * (Decimal(str(slab.tax_rate)) / Decimal("100"))
                
                tax_amount = annual_tax / 12
                
                # Professional Tax
                pt_settings = self.tax_repo.get_active_pt_settings()
                for pt in pt_settings:
                    # Applying the first matching active professional tax
                    if gross_salary >= Decimal(str(pt.salary_threshold)):
                        professional_tax = Decimal(str(pt.monthly_amount))
                        break
                
                net_salary = gross_salary - total_deductions - tax_amount - professional_tax

                record = PayrollRecord(
                    employee_id=emp.id,
                    gross_salary=gross_salary,
                    total_deductions=total_deductions + tax_amount + professional_tax,
                    net_salary=net_salary,
                    pf_amount=pf_amount,
                    tax_amount=tax_amount,
                    professional_tax=professional_tax,
                    items=items
                )
                records.append(record)

                run.total_employees += 1
                run.total_payout += net_salary

            self.db.add(run)
            self.db.flush()

            for rec in records:
                rec.payroll_run_id = run.id
                self.db.add(rec)
                 
            self.db.commit()
            
            return run
        except Exception as e:
            self.db.rollback()
            logger.error(f"Payroll generation failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Payroll generation failed entirely")

    def approve_payroll(self, run_id: int, user_id: int):
        run = self.repo.get_run(run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Payroll run not found")
        if run.status != "GENERATED" and run.status != "REVIEWED":
            raise HTTPException(status_code=400, detail="Invalid status for approval")
        return self.repo.update_run_status(run, "APPROVED", user_id)
        
    def lock_payroll(self, run_id: int, user_id: int):
        run = self.repo.get_run(run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Payroll run not found")
        if run.status != "APPROVED" and run.status != "PAID":
            raise HTTPException(status_code=400, detail="Invalid status for lock")
            
        return self.repo.update_run_status(run, "LOCKED", user_id)
