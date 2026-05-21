from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime

class DeductionRuleBase(BaseModel):
    name: str
    rule_type: str
    calculation_type: str
    percentage: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    fixed_amount: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    max_limit: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    is_active: bool = True

class DeductionRuleCreate(DeductionRuleBase):
    pass

class DeductionRuleUpdate(BaseModel):
    name: Optional[str] = None
    rule_type: Optional[str] = None
    calculation_type: Optional[str] = None
    percentage: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    fixed_amount: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    max_limit: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    is_active: Optional[bool] = None

class DeductionRuleResponse(DeductionRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
