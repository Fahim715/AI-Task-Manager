# AI Task Manager — Prototype

A minimal full-stack app using FastAPI + PostgreSQL + Next.js + Groq AI.

## Stack
- **Backend**: FastAPI (async Python) + asyncpg + PostgreSQL
- **Frontend**: Next.js + TypeScript
- **AI**: Groq LLM API (llama3)
- **DevOps**: Docker Compose

## Quick Start

1. Add your Groq API key in `docker-compose.yml`
2. Run:
   ```bash
   docker-compose up --build
   ```
3. Open http://localhost:3000

## API Endpoints
| Method | Route | Description |
|--------|-------|-------------|
| GET | /tasks | List all tasks |
| POST | /tasks | Create a task |
| PATCH | /tasks/{id}/done | Mark task done |
| DELETE | /tasks/{id} | Delete task |
| GET | /summary | AI summary of tasks |

## Project Structure
```
ai-task-manager/
├── backend/
│   ├── main.py          # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── pages/index.tsx  # Next.js page
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
└── docker-compose.yml
```
