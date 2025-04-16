from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from real_task_prac.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class BaseModel(AsyncAttrs, DeclarativeBase):
    pass


async_engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)

AsyncSession = async_sessionmaker(bind=async_engine, class_=AsyncSession)
