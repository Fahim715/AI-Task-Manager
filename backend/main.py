from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import asyncpg
import os
import httpx

app = FastAPI(title="AI Task Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/taskdb")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

db_pool = None

@app.on_event("startup")
async def startup():
    global db_pool
    db_pool = await asyncpg.create_pool(DATABASE_URL)
    await db_pool.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            done BOOLEAN DEFAULT FALSE
        )
    """)

@app.on_event("shutdown")
async def shutdown():
    await db_pool.close()


# --- Schemas ---
class TaskIn(BaseModel):
    title: str
    description: Optional[str] = ""

class TaskOut(TaskIn):
    id: int
    done: bool


# --- CRUD Routes ---
@app.get("/tasks", response_model=List[TaskOut])
async def get_tasks():
    rows = await db_pool.fetch("SELECT * FROM tasks ORDER BY id DESC")
    return [dict(r) for r in rows]

@app.post("/tasks", response_model=TaskOut)
async def create_task(task: TaskIn):
    row = await db_pool.fetchrow(
        "INSERT INTO tasks (title, description) VALUES ($1, $2) RETURNING *",
        task.title, task.description
    )
    return dict(row)

@app.patch("/tasks/{task_id}/done", response_model=TaskOut)
async def mark_done(task_id: int):
    row = await db_pool.fetchrow(
        "UPDATE tasks SET done=TRUE WHERE id=$1 RETURNING *", task_id
    )
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    return dict(row)

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    await db_pool.execute("DELETE FROM tasks WHERE id=$1", task_id)
    return {"message": "Deleted"}


# --- AI Summary Route ---
@app.get("/summary")
async def ai_summary():
    rows = await db_pool.fetch("SELECT title, description, done FROM tasks")
    if not rows:
        return {"summary": "No tasks yet."}

    task_text = "\n".join(
        [f"- {'[Done]' if r['done'] else '[Pending]'} {r['title']}: {r['description']}" for r in rows]
    )

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": "You are a productivity assistant."},
                    {"role": "user", "content": f"Summarize these tasks briefly:\n{task_text}"}
                ],
                "max_tokens": 200
            }
        )
    data = resp.json()
    return {"summary": data["choices"][0]["message"]["content"]}
