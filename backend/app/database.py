__all__ = ["Base", "get_db_session"]

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

DbNotInitialized = Exception("Database engine is not initialized")


class Base(DeclarativeBase):
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    __mapper_args__ = {"eager_defaults": True}


class DatabaseSessionManager:
    # Heavily inspired by https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html
    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None = None):
        if engine_kwargs is None:
            engine_kwargs = {}

        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(self._engine, class_=AsyncSession)

    async def close(self):
        if not self._engine:
            raise DbNotInitialized

        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if not self._engine:
            raise DbNotInitialized

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception as e:
                await connection.rollback()
                raise e

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if not self._sessionmaker:
            raise DbNotInitialized

        async with self._sessionmaker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()


session_manager = DatabaseSessionManager("sqlite+aiosqlite:///./test.db")


async def get_db_session():
    async with session_manager.session() as session:
        yield session


async def populate_db():
    async with session_manager.connect() as connection:
        await connection.run_sync(Base.metadata.create_all)
