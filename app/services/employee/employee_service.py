from sqlalchemy.orm import Session
from app.repositories.employee_repo import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, PaginatedEmployeeResponse, EmployeeResponse
from fastapi import HTTPException

class EmployeeService:
    def __init__(self, db: Session):
        self.repo = EmployeeRepository(db)

    def create_employee(self, employee_in: EmployeeCreate):
        if self.repo.get_by_code(employee_in.employee_code):
            raise HTTPException(status_code=400, detail="Employee code already exists")
        return self.repo.create(employee_in)

    def get_employees(self, skip: int = 0, limit: int = 100) -> PaginatedEmployeeResponse:
        total = self.repo.count()
        employees = self.repo.get_all(skip=skip, limit=limit)
        return PaginatedEmployeeResponse(
            total=total,
            limit=limit,
            offset=skip,
            data=[EmployeeResponse.model_validate(e) for e in employees]
        )

    def get_employee(self, employee_id: int):
        employee = self.repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee

    def update_employee(self, employee_id: int, employee_in: EmployeeUpdate):
        employee = self.get_employee(employee_id)
        return self.repo.update(employee, employee_in)

    def delete_employee(self, employee_id: int):
        employee = self.get_employee(employee_id)
        return self.repo.delete(employee)
