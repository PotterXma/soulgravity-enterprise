import asyncio
import sys
import os

# Add project root to sys.path
sys.path.append(os.getcwd())

from sqlalchemy import select
from libs.infra_db.session import get_db_session
from libs.infra_db.models.identity import Tenant, User
from libs.security.password import get_password_hash

async def seed():
    print("🌱 Starting data seeding...")
    
    # get_db_session is an async generator, we need to manually iterate or assume context
    # But usually we use it as `async with AsyncSessionLocal() as session:`
    # The helper `get_db_session` yields, so we can't use it directly in `async with` unless it's a context manager.
    # It's defined as a generator: `async def get_db_session(): yield session`.
    # So we should iterate it or just use the session factory directly if accessible.
    # Let's import AsyncSessionLocal from session.py
    from libs.infra_db.session import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        # 1. Seed Tenant
        stmt = select(Tenant).where(Tenant.name == "System")
        result = await session.execute(stmt)
        tenant = result.scalar_one_or_none()

        if not tenant:
            print("Creating 'System' Tenant...")
            tenant = Tenant(id="system", name="System")
            session.add(tenant)
            await session.commit()
            await session.refresh(tenant)
        else:
            print("Found existing 'System' Tenant.")

        # 2. Seed Super Admin
        stmt = select(User).where(User.email == "admin@soulgravity.com")
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            print("Creating 'Super Admin' User...")
            hashed_pwd = get_password_hash("Admin@123")
            user = User(
                email="admin@soulgravity.com",
                password_hash=hashed_pwd,
                is_superuser=True,
                tenant_id=tenant.id # Use tenant.id from the tenant object
            )
            session.add(user)
            await session.commit()
            print("\n✅ Seeding Complete!")
            print("--------------------------------------------------")
            print("Url:      http://localhost")
            print("Username: admin@soulgravity.com")
            print("Password: Admin@123")
            print("--------------------------------------------------")
        else:
            print("Found existing 'Super Admin' User.")
            print("\n✅ Seeding Complete (No changes).")

if __name__ == "__main__":
    asyncio.run(seed())
