from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import User
from schemas.auth import (
    AcceptInviteRequest,
    AuthResponse,
    InviteRequest,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenPair,
)
from services.auth import (
    authenticate_user,
    create_access_token,
    create_invite_token,
    create_org_and_user,
    create_refresh_token,
    create_invited_user,
    decode_token,
)
import os
from services.email import send_email
from routers.deps import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)) -> AuthResponse:
    existing = await db.execute(select(User).where(User.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = await create_org_and_user(db, payload.email, payload.password, payload.org_name)
    await db.commit()
    await db.refresh(user)

    tokens = TokenPair(
        access_token=create_access_token(str(user.id), user.org_id),
        refresh_token=create_refresh_token(str(user.id), user.org_id),
    )
    return AuthResponse(user=user, tokens=tokens)


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> AuthResponse:
    user = await authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    tokens = TokenPair(
        access_token=create_access_token(str(user.id), user.org_id),
        refresh_token=create_refresh_token(str(user.id), user.org_id),
    )
    return AuthResponse(user=user, tokens=tokens)


@router.post("/refresh", response_model=TokenPair)
async def refresh(payload: RefreshRequest) -> TokenPair:
    try:
        token_payload = decode_token(payload.refresh_token)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=401, detail="Invalid refresh token") from exc
    if token_payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = token_payload.get("sub")
    org_id = token_payload.get("org_id")
    return TokenPair(
        access_token=create_access_token(str(user_id), int(org_id)),
        refresh_token=create_refresh_token(str(user_id), int(org_id)),
    )


@router.post("/invite", response_model=dict)
async def invite_user(
    payload: InviteRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    token = create_invite_token(payload.email, current_user.org_id)
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    invite_link = f"{frontend_url}/register?token={token}"
    await send_email(
        payload.email,
        "TaskFlow AI invite",
        f"You have been invited to TaskFlow AI. Use this token to accept: {token}",
    )
    return {"message": "Invite sent", "invite_link": invite_link}


@router.post("/accept-invite", response_model=AuthResponse)
async def accept_invite(payload: AcceptInviteRequest, db: AsyncSession = Depends(get_db)) -> AuthResponse:
    try:
        token_payload = decode_token(payload.token)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail="Invalid invite token") from exc

    if token_payload.get("type") != "invite":
        raise HTTPException(status_code=400, detail="Invalid invite token")

    email = token_payload.get("email")
    org_id = token_payload.get("org_id")

    existing = await db.execute(select(User).where(User.email == email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already exists")

    user = await create_invited_user(db, email, payload.password, int(org_id))
    await db.commit()
    await db.refresh(user)

    tokens = TokenPair(
        access_token=create_access_token(str(user.id), user.org_id),
        refresh_token=create_refresh_token(str(user.id), user.org_id),
    )
    return AuthResponse(user=user, tokens=tokens)
