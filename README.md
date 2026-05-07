# TaskFlow AI

TaskFlow AI is a production-ready, multi-tenant SaaS for AI-powered task and invoice management.

## Feature List
- Multi-tenant organizations with user roles and scoped data.
- JWT access + refresh auth with invite flow.
- Task Kanban board, filtering, and AI-powered suggestions.
- Invoice management with status tracking and task linkage.
- HMAC-signed webhooks with retries and delivery logs.
- Daily overdue checks and weekly email digests via Celery.
- AI summaries and productivity insights using OpenAI.

## Local Setup (Docker)
1. Copy env template:
   ```bash
   cp .env.example .env
   ```
2. Run:
   ```bash
   docker-compose up --build
   ```
3. Open:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000

## Railway Deployment (Backend + DB + Redis)
1. Create a new Railway project.
2. Add PostgreSQL and Redis plugins.
3. Deploy backend service from `backend/` with `backend/railway.toml`.
4. Deploy worker service with `backend/railway.worker.toml`.
5. Deploy beat service with `backend/railway.beat.toml`.
6. Set env vars in Railway (DATABASE_URL, REDIS_URL, SECRET_KEY, OPENAI_API_KEY, SMTP_*).
7. Upload screenshots here:
   - `docs/railway-backend.png`
   - `docs/railway-worker.png`
   - `docs/railway-beat.png`

## Vercel Deployment (Frontend)
1. Import the `frontend/` folder as a new project.
2. Set env var: NEXT_PUBLIC_API_URL to the Railway backend URL.
3. Deploy.

## API Endpoints

### Auth (/api/auth)
| Method | Path | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| POST | /register | No | { email, password, org_name } | { user, tokens } |
| POST | /login | No | { email, password } | { user, tokens } |
| POST | /refresh | No | { refresh_token } | { access_token, refresh_token } |
| POST | /invite | Yes | { email } | { message, invite_link } |
| POST | /accept-invite | No | { token, password } | { user, tokens } |

### Tasks (/api/tasks)
| Method | Path | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| GET | / | Yes | Query: status, assignee_id, due_date, limit, offset | Task[] |
| POST | / | Yes | { title, description, due_date, assignee_id } | Task |
| GET | /{id} | Yes | - | Task |
| PATCH | /{id} | Yes | { title, description, status, due_date, assignee_id, overdue } | Task |
| DELETE | /{id} | Yes | - | { message } |

### Invoices (/api/invoices)
| Method | Path | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| GET | / | Yes | Query: limit, offset | Invoice[] |
| POST | / | Yes | { title, amount, currency, task_id } | Invoice |
| PATCH | /{id} | Yes | { title, amount, currency, status, task_id } | Invoice |
| DELETE | /{id} | Yes | - | { message } |

### Webhooks (/api/webhooks)
| Method | Path | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| GET | / | Yes | - | WebhookConfig[] |
| POST | / | Yes | { url, secret, events, is_active } | WebhookConfig |
| DELETE | /{id} | Yes | - | { message } |
| GET | /logs | Yes | Query: limit, offset | WebhookLog[] |

### AI (/api/ai)
| Method | Path | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| GET | /summary | Yes | - | { summary } |
| POST | /suggest | Yes | { title } | { description, due_date } |
| GET | /insights | Yes | - | { summary } |

## Running Tests
- Backend: `pytest`
- Frontend: `npm run test`

## Architecture Diagram
```
                +------------------+         +----------------------+
                |     Frontend     |         |    Next.js API       |
                |  Vercel / Local  |<------->|  Auth + Proxy Layer  |
                +------------------+         +----------+-----------+
                                                     |
                                                     v
                +------------------+         +----------------------+
                |    FastAPI API   |<------->| PostgreSQL (Railway) |
                |   Railway / Local|         +----------------------+
                +------------------+                 |
                          |                            v
                          |                    +------------------+
                          |                    |  Redis (Railway) |
                          v                    +------------------+
                +------------------+
                |  Celery Workers  |
                |  (webhooks, cron)|
                +------------------+
```
