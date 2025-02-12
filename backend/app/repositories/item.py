from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Item


class ItemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = Item

    async def create(self):
        return {"name": "Item Created"}

    async def get_all(self):
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        return items
