import asyncio
import os
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal
from models import Organization, User, UserRole
from services.auth import hash_password


async def seed() -> None:
    org_name = os.getenv("SEED_ORG_NAME", "TaskFlow AI Demo")
    email = os.getenv("SEED_ADMIN_EMAIL", "admin@taskflow.ai")
    password = os.getenv("SEED_ADMIN_PASSWORD", "ChangeMe123!")

    async with AsyncSessionLocal() as session:
        org = Organization(name=org_name, slug="taskflow-ai-demo")
        session.add(org)
        await session.flush()

        admin = User(
            email=email,
            hashed_password=hash_password(password),
            org_id=org.id,
            role=UserRole.admin,
        )
        session.add(admin)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
