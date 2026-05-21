from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import date

class TaxSlabBase(BaseModel):
    min_income: condecimal(max_digits=15, decimal_places=2)
    max_income: Optional[condecimal(max_digits=15, decimal_places=2)] = None
    tax_rate: condecimal(max_digits=5, decimal_places=2)
    regime_type: str
    effective_from: date
    is_active: bool = True

class TaxSlabCreate(TaxSlabBase):
    pass

class TaxSlabUpdate(BaseModel):
    min_income: Optional[condecimal(max_digits=15, decimal_places=2)] = None
    max_income: Optional[condecimal(max_digits=15, decimal_places=2)] = None
    tax_rate: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    regime_type: Optional[str] = None
    is_active: Optional[bool] = None

class TaxSlabResponse(TaxSlabBase):
    id: int
    
    class Config:
        from_attributes = True

class PfSettingBase(BaseModel):
    employee_contribution: condecimal(max_digits=5, decimal_places=2)
    employer_contribution: condecimal(max_digits=5, decimal_places=2)
    wage_ceiling: condecimal(max_digits=10, decimal_places=2)
    enabled: bool = True
    effective_from: date

class PfSettingResponse(PfSettingBase):
    id: int

    class Config:
        from_attributes = True
