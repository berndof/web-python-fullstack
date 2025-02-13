from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = User

    async def create(self, user_in: UserCreate):
        new_user = User(
            username=user_in.username,
            password=user_in.password,
            first_name=user_in.first_name,
            last_name=user_in.last_name,
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
