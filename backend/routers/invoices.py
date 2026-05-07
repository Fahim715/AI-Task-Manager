from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Invoice, InvoiceStatus
from routers.deps import get_current_user
from schemas.invoice import InvoiceCreate, InvoiceOut, InvoiceUpdate
from workers.webhook_worker import deliver_webhook

router = APIRouter(prefix="/api/invoices", tags=["invoices"])


@router.get("/", response_model=list[InvoiceOut])
async def list_invoices(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> list[InvoiceOut]:
    result = await db.execute(
        select(Invoice)
        .where(Invoice.org_id == current_user.org_id)
        .order_by(Invoice.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return result.scalars().all()


@router.post("/", response_model=InvoiceOut)
async def create_invoice(
    payload: InvoiceCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> InvoiceOut:
    invoice = Invoice(
        title=payload.title,
        amount=payload.amount,
        currency=payload.currency,
        task_id=payload.task_id,
        org_id=current_user.org_id,
    )
    db.add(invoice)
    await db.commit()
    await db.refresh(invoice)
    return invoice


@router.patch("/{invoice_id}", response_model=InvoiceOut)
async def update_invoice(
    invoice_id: int,
    payload: InvoiceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> InvoiceOut:
    result = await db.execute(
        select(Invoice).where(Invoice.id == invoice_id, Invoice.org_id == current_user.org_id)
    )
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(invoice, field, value)

    await db.commit()
    await db.refresh(invoice)

    if invoice.status == InvoiceStatus.paid:
        deliver_webhook.delay(invoice.org_id, "invoice.paid", {"invoice_id": invoice.id})

    return invoice


@router.delete("/{invoice_id}", response_model=dict)
async def delete_invoice(
    invoice_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict:
    result = await db.execute(
        select(Invoice).where(Invoice.id == invoice_id, Invoice.org_id == current_user.org_id)
    )
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    await db.delete(invoice)
    await db.commit()
    return {"message": "Deleted"}
