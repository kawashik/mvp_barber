# app/core/database.py

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from config.config import get_config

config = get_config()


class Base(DeclarativeBase):
    pass


DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{config.db.user}:"
    f"{config.db.password}@"
    f"{config.db.host}:"
    f"{config.db.port}/"
    f"{config.db.name}"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)