import asyncio
from datetime import datetime, timedelta, timezone
from sqlalchemy import select

from celery_app import celery_app
from database import AsyncSessionLocal
from models import Invoice, Organization, Task, TaskStatus, User, UserRole
from services.email import send_email


async def _send_digest() -> int:
    since = datetime.now(timezone.utc) - timedelta(days=7)
    async with AsyncSessionLocal() as session:
        orgs = (await session.execute(select(Organization))).scalars().all()
        count = 0
        for org in orgs:
            tasks_done = (
                await session.execute(
                    select(Task).where(
                        Task.org_id == org.id,
                        Task.status == TaskStatus.done,
                        Task.created_at >= since,
                    )
                )
            ).scalars().all()
            invoices_new = (
                await session.execute(select(Invoice).where(Invoice.org_id == org.id, Invoice.created_at >= since))
            ).scalars().all()
            overdue = (
                await session.execute(select(Task).where(Task.org_id == org.id, Task.overdue.is_(True)))
            ).scalars().all()

            admins = (
                await session.execute(
                    select(User).where(User.org_id == org.id, User.role == UserRole.admin)
                )
            ).scalars().all()

            body = (
                f"Weekly Digest for {org.name}\n"
                f"Completed tasks: {len(tasks_done)}\n"
                f"New invoices: {len(invoices_new)}\n"
                f"Overdue tasks: {len(overdue)}\n"
            )

            for admin in admins:
                await send_email(admin.email, "TaskFlow AI Weekly Digest", body)
                count += 1
        return count


@celery_app.task
def weekly_digest() -> int:
    return asyncio.run(_send_digest())
