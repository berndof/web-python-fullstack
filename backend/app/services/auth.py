from fastapi import HTTPException

from app.repositories import UserRepository
from app.utils import check_password, create_access_token, create_refresh_token
from app.schemas import Token


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def authenticate_user(self, username: str, password: str):
        user = await self.user_repository.get_by_username(username)
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect username")

        if not check_password(password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect password")

        access_token = create_access_token({"sub": user.username})
        refresh_token = create_refresh_token({"sub": user.username})

        return Token(access_token=access_token, refresh_token=refresh_token)
