from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from app.repositories import UserRepository
from app.models import User

from typing import Any
from datetime import timedelta, datetime, UTC

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

import jwt

from fastapi import Depends
from app.core.exceptions import InvalidCredentialsException
from app.schemas import TokenData
from jwt.exceptions import InvalidTokenError

C = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_password_hash(self, password: str) -> str:
        return C.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return C.verify(plain_password, hashed_password)

    async def authenticate_user(self, username: str, password: str) -> User | None:
        user = await self.user_repository.get_by_username(username)
        if not user:
            # Raise user not exists
            return None
        if not self.verify_password(password, user.password):
            return None
            # Raise wrong password
        return user

    def create_access_token(self, data: dict[str, Any], expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.now(UTC) + (expires_delta or timedelta(ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User | None:
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

        user = await self.user_repository.get_by_username(token_data.username)
        if user is None:
            raise InvalidCredentialsException()

        return user
