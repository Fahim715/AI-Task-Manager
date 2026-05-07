import asyncio
import httpx
from celery import shared_task
from sqlalchemy import select

from database import AsyncSessionLocal
from models import WebhookConfig, WebhookLog
from services.webhook import sign_payload


async def _deliver_webhook(webhook_config_id: int, event: str, payload: dict) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(WebhookConfig).where(WebhookConfig.id == webhook_config_id)
        )
        hook = result.scalar_one_or_none()
        if not hook:
            return

        signature = sign_payload(hook.secret, payload)

        status_code = None
        async with httpx.AsyncClient(timeout=10) as client:
            try:
                response = await client.post(
                    hook.url,
                    json=payload,
                    headers={"X-Signature": signature, "X-Event": event},
                )
                status_code = response.status_code
            except httpx.RequestError:
                status_code = None

        log = WebhookLog(
            webhook_config_id=hook.id,
            event=event,
            payload=payload,
            status_code=status_code,
        )
        session.add(log)
        await session.commit()


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def deliver_webhook(self, org_id: int, event: str, payload: dict) -> None:
    try:
        asyncio.run(_deliver_for_org(org_id, event, payload))
    except Exception as exc:  # noqa: BLE001
        countdown = 2 ** self.request.retries
        raise self.retry(exc=exc, countdown=countdown)


async def _deliver_for_org(org_id: int, event: str, payload: dict) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(WebhookConfig).where(
                WebhookConfig.org_id == org_id,
                WebhookConfig.is_active.is_(True),
            )
        )
        hooks = result.scalars().all()

    tasks = []
    for hook in hooks:
        if event not in hook.events:
            continue
        tasks.append(_deliver_webhook(hook.id, event, payload))

    if tasks:
        await asyncio.gather(*tasks)
