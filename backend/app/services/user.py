from app.repositories import UserRepository
from app.schemas import UserCreate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create(self, user_in: UserCreate):
        return await self.repository.create(user_in)
