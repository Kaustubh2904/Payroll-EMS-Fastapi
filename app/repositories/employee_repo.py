from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from typing import List, Optional

class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.id == employee_id).first()
        
    def get_by_code(self, employee_code: str) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.employee_code == employee_code).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        return self.db.query(Employee).offset(skip).limit(limit).all()
        
    def count(self) -> int:
        return self.db.query(Employee).count()

    def create(self, employee_in: EmployeeCreate) -> Employee:
        db_obj = Employee(**employee_in.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: Employee, obj_in: EmployeeUpdate) -> Employee:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: Employee) -> Employee:
        # Soft delete
        db_obj.status = "INACTIVE"
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
