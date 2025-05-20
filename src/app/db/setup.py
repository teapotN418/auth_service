from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from src.app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True
)

async_session_factory = async_sessionmaker(async_engine)

Base = declarative_base()