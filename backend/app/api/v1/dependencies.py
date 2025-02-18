import jwt
from fastapi import Depends
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import ALGORITHM, SECRET_KEY
from app.core.database import get_db_session
from app.core.exceptions import InvalidCredentialsException
from app.core.security import oauth2_schema
from app.repositories import ItemRepository, UserRepository
from app.schemas import TokenData
from app.services import AuthService, ItemService, UserService


async def item_repository(session: AsyncSession = Depends(get_db_session)) -> ItemRepository:
    return ItemRepository(session)


async def item_service(repository: ItemRepository = Depends(item_repository)) -> ItemService:
    return ItemService(repository)


async def user_repository(session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(session)


async def user_service(repository: UserRepository = Depends(user_repository)) -> UserService:
    return UserService(repository)


async def auth_service(user_repository: UserRepository = Depends(user_repository)) -> AuthService:
    return AuthService(user_repository)


async def get_current_user(token: str = Depends(oauth2_schema), user_repo: UserRepository = Depends(user_repository)):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise InvalidCredentialsException()

        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise InvalidCredentialsException()

    if token_data.username is None:
        raise InvalidCredentialsException()

    user = await user_repo.get_by_username(token_data.username)
    if user is None:
        raise InvalidCredentialsException()

    return user
