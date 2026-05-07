from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models import TaskStatus

# ── Auth ────────────────────────────────────────────────
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    tenant_id: str
    created_at: datetime
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# ── Tasks ────────────────────────────────────────────────
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    created_at: datetime
    model_config = {"from_attributes": True}

# ── Invoices ─────────────────────────────────────────────
class InvoiceCreate(BaseModel):
    title: str
    amount: int

class InvoiceOut(BaseModel):
    id: int
    title: str
    amount: int
    paid: bool
    created_at: datetime
    model_config = {"from_attributes": True}
