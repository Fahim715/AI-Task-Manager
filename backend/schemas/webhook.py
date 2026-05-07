from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class WebhookConfigCreate(BaseModel):
    url: HttpUrl
    secret: str
    events: List[str]
    is_active: bool = True


class WebhookConfigOut(BaseModel):
    id: int
    org_id: int
    url: HttpUrl
    events: List[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}


class WebhookLogOut(BaseModel):
    id: int
    webhook_config_id: int
    event: str
    payload: dict
    status_code: Optional[int]
    delivered_at: datetime

    model_config = {"from_attributes": True}
