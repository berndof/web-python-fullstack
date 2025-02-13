from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.repositories import ItemRepository
from app.services import ItemService


async def item_repository(session: AsyncSession = Depends(get_db_session)) -> ItemRepository:
    return ItemRepository(session)


async def item_service(repository: ItemRepository = Depends(item_repository)) -> ItemService:
    return ItemService(repository)
