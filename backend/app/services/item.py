from app.repositories import ItemRepository


class ItemService:
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    async def create(self):
        return await self.repository.create()

    async def get_all(self):
        return await self.repository.get_all()
