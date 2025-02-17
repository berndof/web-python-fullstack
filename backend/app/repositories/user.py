from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import User
from app.schemas import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = User

    async def get_by_username(self, username: str) -> User | None:
        """Retrieve a user by their username.

        Args:
            username (str): The username of the user to be retrieved.

        Returns:
            User | None: The user object if found, otherwise None.
        """

        selection_query = select(self.model).where(self.model.username == username)
        result = await self.session.execute(selection_query)
        return result.scalar_one_or_none()

    async def create(self, user_in: UserCreate):
        exists = await self.get_by_username(user_in.username)
        if exists:
            raise HTTPException(status_code=400, detail="User already exists")

        new_user = User(
            username=user_in.username,
            password=user_in.password,
            first_name=user_in.first_name,
            last_name=user_in.last_name,
        )
        self.session.add(new_user)
        await self.session.refresh(new_user)
        return new_user
