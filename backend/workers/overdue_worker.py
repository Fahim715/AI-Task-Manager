import asyncio
from datetime import datetime, timezone
from celery import shared_task
from sqlalchemy import select

from database import AsyncSessionLocal
from models import Task


async def _mark_overdue() -> int:
    now = datetime.now(timezone.utc)
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Task).where(Task.due_date.is_not(None)))
        tasks = result.scalars().all()
        count = 0
        for task in tasks:
            if task.due_date and task.due_date < now and not task.overdue:
                task.overdue = True
                count += 1
        await session.commit()
        return count


@shared_task
def daily_overdue_check() -> int:
    return asyncio.run(_mark_overdue())
