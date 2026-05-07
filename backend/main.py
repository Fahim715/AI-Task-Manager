from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from routers.ai import router as ai_router
from routers.auth import router as auth_router
from routers.invoices import router as invoices_router
from routers.tasks import router as tasks_router
from routers.webhooks import router as webhooks_router

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI(title="TaskFlow AI")
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail, "code": exc.status_code})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"error": "Validation error", "code": 422, "details": exc.errors()})


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(_: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(status_code=429, content={"error": "Rate limit exceeded", "code": 429})


app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(invoices_router)
app.include_router(webhooks_router)
app.include_router(ai_router)


@app.get("/api/health", response_model=dict)
async def health() -> dict:
    return {"status": "ok"}
