from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Task
from routers.deps import get_current_user
from schemas.ai import AISuggestRequest, AISuggestResponse, AISummaryResponse, AIInsightsResponse
from services.ai import build_weekly_insights, embed_task_titles, suggest_task_details, summarize_tasks

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.get("/summary", response_model=AISummaryResponse)
async def summary(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> AISummaryResponse:
    result = await db.execute(select(Task).where(Task.org_id == current_user.org_id))
    tasks = result.scalars().all()
    summary_text = await summarize_tasks(tasks)
    return AISummaryResponse(summary=summary_text)


@router.post("/suggest", response_model=AISuggestResponse)
async def suggest(
    payload: AISuggestRequest,
    current_user=Depends(get_current_user),
) -> AISuggestResponse:
    description, due_date = await suggest_task_details(payload.title)
    return AISuggestResponse(description=description, due_date=due_date)


@router.get("/insights", response_model=AIInsightsResponse)
async def insights(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> AIInsightsResponse:
    result = await db.execute(select(Task).where(Task.org_id == current_user.org_id))
    tasks = result.scalars().all()

    done = len([task for task in tasks if task.status.value == "done"])
    pending = len([task for task in tasks if task.status.value != "done"])
    overdue = len([task for task in tasks if task.overdue])

    assignee_counts = {}
    for task in tasks:
        assignee_counts[task.assignee_id] = assignee_counts.get(task.assignee_id, 0) + 1

    await embed_task_titles(tasks)

    metrics = {
        "done": done,
        "pending": pending,
        "overdue": overdue,
        "busiest_assignee": max(assignee_counts, key=assignee_counts.get) if assignee_counts else None,
    }
    summary = await summarize_tasks(tasks)
    narrative = await build_weekly_insights(summary, metrics)
    return AIInsightsResponse(summary=narrative)
