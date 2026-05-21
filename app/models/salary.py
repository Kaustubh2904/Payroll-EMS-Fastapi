from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class SalaryStructure(Base):
    __tablename__ = "salary_structures"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    grade = Column(String(50))
    status = Column(String(50), default="ACTIVE")
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    components = relationship("SalaryComponent", back_populates="structure")

class SalaryComponent(Base):
    __tablename__ = "salary_components"

    id = Column(Integer, primary_key=True, index=True)
    salary_structure_id = Column(Integer, ForeignKey("salary_structures.id"), nullable=False)
    component_name = Column(String(255), nullable=False)
    component_type = Column(String(50), nullable=False) # earning / deduction
    calculation_type = Column(String(50), nullable=False) # fixed / percentage
    amount = Column(Numeric(10, 2), nullable=False)
    is_taxable = Column(Boolean, default=True)
    is_pf_applicable = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    structure = relationship("SalaryStructure", back_populates="components")

class EmployeeSalaryAssignment(Base):
    __tablename__ = "employee_salary_assignments"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    salary_structure_id = Column(Integer, ForeignKey("salary_structures.id"), nullable=False)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
