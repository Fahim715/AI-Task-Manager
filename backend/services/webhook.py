import hashlib
import hmac
import json
from typing import Iterable
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import WebhookConfig


def sign_payload(secret: str, payload: dict) -> str:
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), raw, hashlib.sha256).hexdigest()
    return f"sha256={signature}"


async def get_active_webhooks(db: AsyncSession, org_id: int, event: str) -> Iterable[WebhookConfig]:
    result = await db.execute(
        select(WebhookConfig).where(
            WebhookConfig.org_id == org_id,
            WebhookConfig.is_active.is_(True),
        )
    )
    webhooks = result.scalars().all()
    return [hook for hook in webhooks if event in hook.events]
