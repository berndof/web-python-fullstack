from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.repositories import ItemRepository, UserRepository
from app.services import ItemService, UserService


async def item_repository(session: AsyncSession = Depends(get_db_session)) -> ItemRepository:
    return ItemRepository(session)


async def item_service(repository: ItemRepository = Depends(item_repository)) -> ItemService:
    return ItemService(repository)


async def user_repository(session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(session)


async def user_service(repository: UserRepository = Depends(user_repository)) -> UserService:
    return UserService(repository)
