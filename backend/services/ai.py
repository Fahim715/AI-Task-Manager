import os
from datetime import datetime, timezone
from typing import Sequence
import httpx

from models import Task

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
OPENAI_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")


def _auth_headers() -> dict:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    return {"Authorization": f"Bearer {OPENAI_API_KEY}"}


async def summarize_tasks(tasks: Sequence[Task]) -> str:
    """Summarize tasks using OpenAI chat completions."""
    if not tasks:
        return "No tasks yet."

    lines = []
    for task in tasks:
        status = task.status.value
        due = task.due_date.astimezone(timezone.utc).date().isoformat() if task.due_date else "no due date"
        lines.append(f"- [{status}] {task.title} (due {due})")

    payload = {
        "model": OPENAI_CHAT_MODEL,
        "messages": [
            {"role": "system", "content": "You summarize task lists for busy teams."},
            {"role": "user", "content": "Summarize these tasks in 3 bullet points:\n" + "\n".join(lines)},
        ],
        "max_tokens": 250,
    }
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(
            f"{OPENAI_BASE_URL}/chat/completions",
            headers=_auth_headers(),
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


async def suggest_task_details(title: str) -> tuple[str, str]:
    """Suggest task description and due date using OpenAI chat completions."""
    payload = {
        "model": OPENAI_CHAT_MODEL,
        "messages": [
            {"role": "system", "content": "Suggest helpful task details for a project manager."},
            {"role": "user", "content": f"Provide a description and due date for: {title}."},
        ],
        "max_tokens": 150,
    }
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(
            f"{OPENAI_BASE_URL}/chat/completions",
            headers=_auth_headers(),
            json=payload,
        )
        response.raise_for_status()
        data = response.json()["choices"][0]["message"]["content"]

    lines = [line.strip() for line in data.split("\n") if line.strip()]
    description = lines[0] if lines else ""
    due_date = lines[1] if len(lines) > 1 else datetime.now(timezone.utc).date().isoformat()
    return description, due_date


async def embed_task_titles(tasks: Sequence[Task]) -> list[list[float]]:
    """Generate embeddings for task titles."""
    if not tasks:
        return []

    payload = {
        "model": OPENAI_EMBED_MODEL,
        "input": [task.title for task in tasks],
    }
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(
            f"{OPENAI_BASE_URL}/embeddings",
            headers=_auth_headers(),
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        return [item["embedding"] for item in data["data"]]


async def build_weekly_insights(summary: str, metrics: dict) -> str:
    """Generate narrative insights combining stats and AI."""
    payload = {
        "model": OPENAI_CHAT_MODEL,
        "messages": [
            {"role": "system", "content": "Write a concise weekly productivity summary."},
            {
                "role": "user",
                "content": "Metrics: " + str(metrics) + "\nSummary: " + summary,
            },
        ],
        "max_tokens": 200,
    }
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(
            f"{OPENAI_BASE_URL}/chat/completions",
            headers=_auth_headers(),
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
