from sqlalchemy.orm import Session
from app.models.deduction import DeductionRule
from app.schemas.deduction import DeductionRuleCreate, DeductionRuleUpdate
from typing import List, Optional

class DeductionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, rule_id: int) -> Optional[DeductionRule]:
        return self.db.query(DeductionRule).filter(DeductionRule.id == rule_id).first()

    def get_all(self, active_only: bool = False) -> List[DeductionRule]:
        query = self.db.query(DeductionRule)
        if active_only:
            query = query.filter(DeductionRule.is_active == True)
        return query.all()

    def create(self, rule_in: DeductionRuleCreate) -> DeductionRule:
        rule = DeductionRule(**rule_in.model_dump())
        self.db.add(rule)
        self.db.commit()
        self.db.refresh(rule)
        return rule

    def update(self, db_obj: DeductionRule, obj_in: DeductionRuleUpdate) -> DeductionRule:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
