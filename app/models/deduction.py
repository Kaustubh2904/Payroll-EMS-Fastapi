from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric
from sqlalchemy.sql import func
from app.models.base import Base

class DeductionRule(Base):
    __tablename__ = "deduction_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    rule_type = Column(String(100), nullable=False)
    calculation_type = Column(String(50), nullable=False) # fixed / percentage
    percentage = Column(Numeric(5, 2))
    fixed_amount = Column(Numeric(10, 2))
    max_limit = Column(Numeric(10, 2))
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
