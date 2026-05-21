from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

class EmployeeBase(BaseModel):
    employee_code: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    joining_date: date
    bank_account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    pan_number: Optional[str] = None
    department_id: Optional[int] = None
    designation_id: Optional[int] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    bank_account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    pan_number: Optional[str] = None
    status: Optional[str] = None

class EmployeeResponse(EmployeeBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedEmployeeResponse(BaseModel):
    total: int
    limit: int
    offset: int
    data: list[EmployeeResponse]
