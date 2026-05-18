## database.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
import os


DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./portfolio.db")

# Render gives postgres:// but SQLAlchemy needs postgresql+asyncpg://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./portfolio.db"

# engine = create_async_engine(
#     SQLALCHEMY_DATABASE_URL,
#     connect_args={"check_same_thread": False},
# )

# AsyncSessionLocal = async_sessionmaker(
#     engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
# )


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


