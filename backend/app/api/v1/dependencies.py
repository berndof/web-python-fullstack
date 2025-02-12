from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.repositories.item import ItemRepository


async def get_item_repository(session: AsyncSession = Depends(get_db_session)) -> ItemRepository:
    return ItemRepository(session)
