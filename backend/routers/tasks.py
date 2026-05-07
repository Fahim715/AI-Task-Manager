from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Task, TaskStatus
from routers.deps import get_current_user
from schemas.task import TaskCreate, TaskOut, TaskUpdate
from workers.webhook_worker import deliver_webhook

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskOut])
async def list_tasks(
    status: TaskStatus | None = None,
    assignee_id: int | None = None,
    due_date: date | None = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> list[TaskOut]:
    query = select(Task).where(Task.org_id == current_user.org_id)
    if status:
        query = query.where(Task.status == status)
    if assignee_id:
        query = query.where(Task.assignee_id == assignee_id)
    if due_date:
        query = query.where(Task.due_date >= due_date)

    result = await db.execute(query.order_by(Task.created_at.desc()).limit(limit).offset(offset))
    return result.scalars().all()


@router.post("/", response_model=TaskOut)
async def create_task(
    payload: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> TaskOut:
    task = Task(
        title=payload.title,
        description=payload.description,
        due_date=payload.due_date,
        assignee_id=payload.assignee_id,
        org_id=current_user.org_id,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)

    deliver_webhook.delay(task.org_id, "task.created", {"task_id": task.id, "title": task.title})
    return task


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> TaskOut:
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.org_id == current_user.org_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> TaskOut:
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.org_id == current_user.org_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)

    deliver_webhook.delay(task.org_id, "task.updated", {"task_id": task.id, "title": task.title})
    return task


@router.delete("/{task_id}", response_model=dict)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict:
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.org_id == current_user.org_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()

    deliver_webhook.delay(current_user.org_id, "task.deleted", {"task_id": task_id})
    return {"message": "Deleted"}
