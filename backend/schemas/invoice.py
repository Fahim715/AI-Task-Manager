from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from models.invoice import InvoiceStatus


class InvoiceCreate(BaseModel):
    title: str
    amount: float
    currency: str = "BDT"
    task_id: Optional[int] = None


class InvoiceUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    status: Optional[InvoiceStatus] = None
    task_id: Optional[int] = None


class InvoiceOut(BaseModel):
    id: int
    title: str
    amount: float
    currency: str
    status: InvoiceStatus
    task_id: Optional[int]
    org_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}
