from pydantic import BaseModel, condecimal
from typing import Optional, List, Dict, Any
from datetime import datetime

class PayrollRunBase(BaseModel):
    month: int
    year: int

class PayrollRunCreate(PayrollRunBase):
    pass

class PayrollItemResponse(BaseModel):
    id: int
    component_name: str
    component_type: str
    amount: condecimal(max_digits=10, decimal_places=2)

    class Config:
        from_attributes = True

class PayrollRecordResponse(BaseModel):
    id: int
    employee_id: int
    gross_salary: condecimal(max_digits=15, decimal_places=2)
    total_deductions: condecimal(max_digits=15, decimal_places=2)
    net_salary: condecimal(max_digits=15, decimal_places=2)
    pf_amount: condecimal(max_digits=10, decimal_places=2)
    tax_amount: condecimal(max_digits=10, decimal_places=2)
    professional_tax: condecimal(max_digits=10, decimal_places=2)
    status: str
    items: List[PayrollItemResponse]

    class Config:
        from_attributes = True

class PayrollRunResponse(PayrollRunBase):
    id: int
    status: str
    total_employees: int
    total_payout: condecimal(max_digits=15, decimal_places=2)
    processed_by: int
    approved_by: Optional[int] = None
    created_at: datetime
    approved_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        
class PayrollRunDetailsResponse(PayrollRunResponse):
    records: List[PayrollRecordResponse]
