from datetime import datetime, timedelta, timezone
import os
import secrets
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Organization, User, UserRole

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
INVITE_TOKEN_EXPIRE_HOURS = int(os.getenv("INVITE_TOKEN_EXPIRE_HOURS", "48"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password for storage."""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain-text password against its hash."""
    return pwd_context.verify(plain, hashed)


def create_access_token(subject: str, org_id: int) -> str:
    """Create a signed JWT access token."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "org_id": org_id, "exp": expire, "type": "access"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(subject: str, org_id: int) -> str:
    """Create a signed JWT refresh token."""
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": subject, "org_id": org_id, "exp": expire, "type": "refresh"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_invite_token(email: str, org_id: int) -> str:
    """Create a signed invite token for new users."""
    expire = datetime.now(timezone.utc) + timedelta(hours=INVITE_TOKEN_EXPIRE_HOURS)
    payload = {
        "email": email,
        "org_id": org_id,
        "exp": expire,
        "type": "invite",
        "nonce": secrets.token_hex(8),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode a JWT token and return its claims."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    """Authenticate user credentials and return a user when valid."""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


async def create_org_and_user(db: AsyncSession, email: str, password: str, org_name: str) -> User:
    """Create an organization and its first admin user."""
    base_slug = org_name.strip().lower().replace(" ", "-") or "org"
    slug = base_slug
    counter = 1
    while True:
        result = await db.execute(select(Organization).where(Organization.slug == slug))
        if not result.scalar_one_or_none():
            break
        counter += 1
        slug = f"{base_slug}-{counter}"

    org = Organization(name=org_name, slug=slug)
    db.add(org)
    await db.flush()
    user = User(
        email=email,
        hashed_password=hash_password(password),
        org_id=org.id,
        role=UserRole.admin,
    )
    db.add(user)
    await db.flush()
    return user


async def create_invited_user(db: AsyncSession, email: str, password: str, org_id: int) -> User:
    """Create a user from an invite token."""
    user = User(
        email=email,
        hashed_password=hash_password(password),
        org_id=org_id,
        role=UserRole.member,
    )
    db.add(user)
    await db.flush()
    return user
