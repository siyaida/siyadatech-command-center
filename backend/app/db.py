"""Async SQLAlchemy database setup."""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

# Convert postgresql:// to postgresql+asyncpg://
DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def init_db():
    """Create tables on startup."""
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.create_all)
        pass  # Use Alembic migrations in production

async def get_db() -> AsyncSession:
    """Dependency for FastAPI endpoints."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
