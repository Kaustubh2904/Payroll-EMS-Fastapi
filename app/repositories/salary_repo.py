from sqlalchemy.orm import Session
from app.models.salary import SalaryStructure, SalaryComponent, EmployeeSalaryAssignment
from app.schemas.salary import SalaryStructureCreate, SalaryStructureUpdate, StructureAssignmentCreate
from typing import List, Optional
from datetime import date

class SalaryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_structure(self, structure_in: SalaryStructureCreate) -> SalaryStructure:
        db_structure = SalaryStructure(
            name=structure_in.name,
            grade=structure_in.grade,
            status=structure_in.status,
            effective_from=structure_in.effective_from,
            effective_to=structure_in.effective_to
        )
        self.db.add(db_structure)
        self.db.flush()

        for comp in structure_in.components:
            db_comp = SalaryComponent(
                salary_structure_id=db_structure.id,
                **comp.model_dump()
            )
            self.db.add(db_comp)
            
        self.db.commit()
        self.db.refresh(db_structure)
        return db_structure

    def get_structure(self, id: int) -> Optional[SalaryStructure]:
        return self.db.query(SalaryStructure).filter(SalaryStructure.id == id).first()

    def list_structures(self) -> List[SalaryStructure]:
        return self.db.query(SalaryStructure).all()

    def update_structure(self, db_obj: SalaryStructure, obj_in: SalaryStructureUpdate) -> SalaryStructure:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def assign_structure(self, assignment_in: StructureAssignmentCreate) -> EmployeeSalaryAssignment:
        # deactivate previous active structures for employee
        active_assignments = self.db.query(EmployeeSalaryAssignment).filter(
            EmployeeSalaryAssignment.employee_id == assignment_in.employee_id,
            EmployeeSalaryAssignment.is_active == True
        ).all()
        for assignment in active_assignments:
            assignment.is_active = False
            assignment.effective_to = date.today()
            self.db.add(assignment)

        db_assignment = EmployeeSalaryAssignment(**assignment_in.model_dump())
        self.db.add(db_assignment)
        self.db.commit()
        self.db.refresh(db_assignment)
        return db_assignment
        
    def get_active_assignment(self, employee_id: int) -> Optional[EmployeeSalaryAssignment]:
        return self.db.query(EmployeeSalaryAssignment).filter(
            EmployeeSalaryAssignment.employee_id == employee_id,
            EmployeeSalaryAssignment.is_active == True
        ).first()

