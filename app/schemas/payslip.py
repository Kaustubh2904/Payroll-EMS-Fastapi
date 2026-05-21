from pydantic import BaseModel
from datetime import datetime

class PayslipResponse(BaseModel):
    id: int
    payroll_record_id: int
    file_url: str
    generated_at: datetime

    class Config:
        from_attributes = True