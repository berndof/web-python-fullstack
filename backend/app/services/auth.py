from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.core.exceptions import InvalidCredentialsException
from app.core.security import verify_password
from app.models import User
from app.repositories.user import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.user_repository.get_by_username(username)
        if not user:
            raise InvalidCredentialsException(message="User not found")
        if not verify_password(password, user.password):
            raise InvalidCredentialsException(message="Invalid password")
        return user

    def create_access_token(self, data: dict[str, Any], expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.now(UTC) + (expires_delta or timedelta(ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
