from sqlalchemy.ext.asyncio import AsyncSession


class ItemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self):
        return {"name": "Item Created"}
