from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel, condecimal

class SalaryComponentBase(BaseModel):
    component_name: str
    component_type: str
    calculation_type: str
    amount: condecimal(max_digits=10, decimal_places=2)
    is_taxable: bool = True
    is_pf_applicable: bool = False

class SalaryComponentCreate(SalaryComponentBase):
    pass

class SalaryComponentResponse(SalaryComponentBase):
    id: int
    salary_structure_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class SalaryStructureBase(BaseModel):
    name: str
    grade: Optional[str] = None
    status: str = "ACTIVE"
    effective_from: date
    effective_to: Optional[date] = None

class SalaryStructureCreate(SalaryStructureBase):
    components: List[SalaryComponentCreate]

class SalaryStructureUpdate(BaseModel):
    name: Optional[str] = None
    grade: Optional[str] = None
    status: Optional[str] = None
    effective_to: Optional[date] = None

class SalaryStructureResponse(SalaryStructureBase):
    id: int
    created_at: datetime
    updated_at: datetime
    components: List[SalaryComponentResponse]
    
    class Config:
        from_attributes = True

class StructureAssignmentBase(BaseModel):
    employee_id: int
    salary_structure_id: int
    effective_from: date
    effective_to: Optional[date] = None

class StructureAssignmentCreate(StructureAssignmentBase):
    pass
