from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Numeric
from sqlalchemy.sql import func
from app.models.base import Base

class TaxSlab(Base):
    __tablename__ = "tax_slabs"

    id = Column(Integer, primary_key=True, index=True)
    min_income = Column(Numeric(15, 2), nullable=False)
    max_income = Column(Numeric(15, 2), nullable=True)
    tax_rate = Column(Numeric(5, 2), nullable=False)
    regime_type = Column(String(50), nullable=False) # e.g. OLD or NEW
    effective_from = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

class PfSetting(Base):
    __tablename__ = "pf_settings"

    id = Column(Integer, primary_key=True, index=True)
    employee_contribution = Column(Numeric(5, 2), nullable=False)
    employer_contribution = Column(Numeric(5, 2), nullable=False)
    wage_ceiling = Column(Numeric(10, 2), nullable=False)
    enabled = Column(Boolean, default=True)
    effective_from = Column(Date, nullable=False)

class ProfessionalTaxSetting(Base):
    __tablename__ = "professional_tax_settings"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(String(100), nullable=False)
    monthly_amount = Column(Numeric(10, 2), nullable=False)
    salary_threshold = Column(Numeric(10, 2), nullable=False)
    effective_from = Column(Date, nullable=False)
