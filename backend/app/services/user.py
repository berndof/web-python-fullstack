from app.core.exceptions import UserAlreadyExistsException
from app.repositories import UserRepository
from app.schemas import UserCreate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create(self, user_in: UserCreate):
        exists = await self.repository.get_by_username(user_in.username)
        if exists:
            raise UserAlreadyExistsException()
        new_user = await self.repository.create(user_in)
        return new_user
