from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse, PaginatedEmployeeResponse
from app.services.employee.employee_service import EmployeeService
from app.api.dependencies import get_current_active_hr_admin

router = APIRouter()

def get_employee_service(db: Session = Depends(get_db)):
    return EmployeeService(db)

@router.post("", response_model=EmployeeResponse)
def create_employee(
    employee_in: EmployeeCreate,
    service: EmployeeService = Depends(get_employee_service),
    current_user = Depends(get_current_active_hr_admin)
):
    return service.create_employee(employee_in)

@router.get("", response_model=PaginatedEmployeeResponse)
def list_employees(
    skip: int = 0,
    limit: int = 100,
    service: EmployeeService = Depends(get_employee_service),
    current_user = Depends(get_current_active_hr_admin)
):
    return service.get_employees(skip, limit)

@router.get("/{id}", response_model=EmployeeResponse)
def get_employee(
    id: int,
    service: EmployeeService = Depends(get_employee_service),
    current_user = Depends(get_current_active_hr_admin)
):
    return service.get_employee(id)

@router.put("/{id}", response_model=EmployeeResponse)
def update_employee(
    id: int,
    employee_in: EmployeeUpdate,
    service: EmployeeService = Depends(get_employee_service),
    current_user = Depends(get_current_active_hr_admin)
):
    return service.update_employee(id, employee_in)

@router.delete("/{id}", response_model=EmployeeResponse)
def delete_employee(
    id: int,
    service: EmployeeService = Depends(get_employee_service),
    current_user = Depends(get_current_active_hr_admin)
):
    return service.delete_employee(id)
