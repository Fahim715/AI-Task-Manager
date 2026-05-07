from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import WebhookConfig, WebhookLog
from routers.deps import get_current_user
from schemas.webhook import WebhookConfigCreate, WebhookConfigOut, WebhookLogOut

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


@router.get("/", response_model=list[WebhookConfigOut])
async def list_webhooks(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> list[WebhookConfigOut]:
    result = await db.execute(select(WebhookConfig).where(WebhookConfig.org_id == current_user.org_id))
    return result.scalars().all()


@router.post("/", response_model=WebhookConfigOut)
async def create_webhook(
    payload: WebhookConfigCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> WebhookConfigOut:
    hook = WebhookConfig(
        org_id=current_user.org_id,
        url=str(payload.url),
        secret=payload.secret,
        events=payload.events,
        is_active=payload.is_active,
    )
    db.add(hook)
    await db.commit()
    await db.refresh(hook)
    return hook


@router.delete("/{hook_id}", response_model=dict)
async def delete_webhook(
    hook_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict:
    result = await db.execute(
        select(WebhookConfig).where(WebhookConfig.id == hook_id, WebhookConfig.org_id == current_user.org_id)
    )
    hook = result.scalar_one_or_none()
    if not hook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    await db.delete(hook)
    await db.commit()
    return {"message": "Deleted"}


@router.get("/logs", response_model=list[WebhookLogOut])
async def list_logs(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> list[WebhookLogOut]:
    result = await db.execute(
        select(WebhookLog)
        .join(WebhookConfig, WebhookConfig.id == WebhookLog.webhook_config_id)
        .where(WebhookConfig.org_id == current_user.org_id)
        .order_by(WebhookLog.delivered_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return result.scalars().all()
