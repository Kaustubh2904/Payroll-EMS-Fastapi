from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class PayrollRun(Base):
    __tablename__ = "payroll_runs"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    status = Column(String(50), default="DRAFT") # DRAFT, GENERATED, REVIEWED, APPROVED, EXPORTED, PAID, LOCKED
    total_employees = Column(Integer, default=0)
    total_payout = Column(Numeric(15, 2), default=0.00)
    processed_by = Column(Integer, ForeignKey("users.id"))
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    approved_at = Column(DateTime(timezone=True), nullable=True)

    records = relationship("PayrollRecord", back_populates="payroll_run")


class PayrollRecord(Base):
    __tablename__ = "payroll_records"

    id = Column(Integer, primary_key=True, index=True)
    payroll_run_id = Column(Integer, ForeignKey("payroll_runs.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    gross_salary = Column(Numeric(15, 2), nullable=False)
    total_deductions = Column(Numeric(15, 2), nullable=False)
    net_salary = Column(Numeric(15, 2), nullable=False)
    pf_amount = Column(Numeric(10, 2), nullable=False)
    tax_amount = Column(Numeric(10, 2), nullable=False)
    professional_tax = Column(Numeric(10, 2), nullable=False)
    status = Column(String(50), default="GENERATED")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    payroll_run = relationship("PayrollRun", back_populates="records")
    items = relationship("PayrollItem", back_populates="record")
    employee = relationship("Employee")


class PayrollItem(Base):
    __tablename__ = "payroll_items"

    id = Column(Integer, primary_key=True, index=True)
    payroll_record_id = Column(Integer, ForeignKey("payroll_records.id"), nullable=False)
    component_name = Column(String(255), nullable=False)
    component_type = Column(String(50), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    metadata_json = Column(JSON, nullable=True) # renamed to avoid reserved keywords in some DBs
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    record = relationship("PayrollRecord", back_populates="items")


class Payslip(Base):
    __tablename__ = "payslips"

    id = Column(Integer, primary_key=True, index=True)
    payroll_record_id = Column(Integer, ForeignKey("payroll_records.id"), nullable=False)
    file_url = Column(String(500), nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    
class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(255), nullable=False)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(Integer, nullable=False)
    metadata_json = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
