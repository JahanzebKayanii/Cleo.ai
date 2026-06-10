from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

_connect_args = {"ssl": "require"} if not settings.is_dev else {}

engine = create_async_engine(
    settings.database_url,
    echo=settings.is_dev,
    pool_pre_ping=True,
    connect_args=_connect_args,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@asynccontextmanager
async def get_db_context():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Add new columns that don't exist yet (safe to run every startup)
        migrations = [
            "ALTER TABLE business ADD COLUMN IF NOT EXISTS service_area TEXT DEFAULT 'Austin, TX and surrounding areas within 30 miles'",
            "ALTER TABLE business ADD COLUMN IF NOT EXISTS owner_email VARCHAR(255)",
            "ALTER TABLE business ADD COLUMN IF NOT EXISTS transfer_phone VARCHAR(20)",
            # Multi-tenant columns
            "ALTER TABLE business ADD COLUMN IF NOT EXISTS twilio_phone_number VARCHAR(20)",
            "ALTER TABLE business ADD COLUMN IF NOT EXISTS slug VARCHAR(50)",
            "ALTER TABLE business ADD COLUMN IF NOT EXISTS dashboard_password VARCHAR(255)",
            "ALTER TABLE business ADD COLUMN IF NOT EXISTS industry VARCHAR(50) DEFAULT 'hvac'",
            "ALTER TABLE business ADD COLUMN IF NOT EXISTS qdrant_collection VARCHAR(100)",
            "ALTER TABLE business ADD COLUMN IF NOT EXISTS google_calendar_id TEXT",
            "ALTER TABLE business ADD COLUMN IF NOT EXISTS google_service_account_b64 TEXT",
            "ALTER TABLE business ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE",
            "ALTER TABLE business ADD COLUMN IF NOT EXISTS stripe_customer_id VARCHAR(100)",
            "ALTER TABLE business ADD COLUMN IF NOT EXISTS stripe_subscription_id VARCHAR(100)",
            # Scope calls and documents to a tenant
            "ALTER TABLE calls ADD COLUMN IF NOT EXISTS business_id INTEGER REFERENCES business(id)",
            "ALTER TABLE documents ADD COLUMN IF NOT EXISTS business_id INTEGER REFERENCES business(id) DEFAULT 1",
            # Back-fill existing rows to tenant 1
            "UPDATE calls SET business_id = 1 WHERE business_id IS NULL",
            "UPDATE documents SET business_id = 1 WHERE business_id IS NULL",
            # Scope customers to a tenant
            "ALTER TABLE customers ADD COLUMN IF NOT EXISTS business_id INTEGER REFERENCES business(id)",
            "UPDATE customers SET business_id = 1 WHERE business_id IS NULL",
            # The old unique constraint on (phone) must be dropped before the new composite constraint applies
            "ALTER TABLE customers DROP CONSTRAINT IF EXISTS customers_phone_key",
            # Add the composite unique constraint (safe to run repeatedly)
            "ALTER TABLE customers DROP CONSTRAINT IF EXISTS uq_customer_business_phone",
            "ALTER TABLE customers ADD CONSTRAINT uq_customer_business_phone UNIQUE (business_id, phone)",
        ]
        for sql in migrations:
            await conn.execute(text(sql))
