from sqlalchemy.orm import Session
from app.models.tax import TaxSlab, PfSetting, ProfessionalTaxSetting
from app.schemas.tax import TaxSlabCreate, TaxSlabUpdate
from typing import List, Optional

class TaxRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_slab(self, slab_id: int) -> Optional[TaxSlab]:
        return self.db.query(TaxSlab).filter(TaxSlab.id == slab_id).first()

    def list_slabs(self, regime_type: Optional[str] = None, active_only: bool = True) -> List[TaxSlab]:
        query = self.db.query(TaxSlab)
        if regime_type:
            query = query.filter(TaxSlab.regime_type == regime_type)
        if active_only:
            query = query.filter(TaxSlab.is_active == True)
        return query.order_by(TaxSlab.min_income.asc()).all()

    def create_slab(self, slab_in: TaxSlabCreate) -> TaxSlab:
        slab = TaxSlab(**slab_in.model_dump())
        self.db.add(slab)
        self.db.commit()
        self.db.refresh(slab)
        return slab

    def update_slab(self, db_obj: TaxSlab, obj_in: TaxSlabUpdate) -> TaxSlab:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get_active_pf_setting(self) -> Optional[PfSetting]:
        return self.db.query(PfSetting).filter(PfSetting.enabled == True).order_by(PfSetting.effective_from.desc()).first()
        
    def get_active_pt_settings(self) -> List[ProfessionalTaxSetting]:
        return self.db.query(ProfessionalTaxSetting).order_by(ProfessionalTaxSetting.salary_threshold.desc()).all()
