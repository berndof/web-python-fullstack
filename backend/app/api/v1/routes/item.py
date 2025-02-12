from fastapi import APIRouter, Depends

from app.api.v1.dependencies import item_repository

router = APIRouter(prefix="/item", tags=["item"])


@router.get("/get_items")
async def get_items(repository=Depends(item_repository)):  # type: ignore
    return await repository.get_items()


@router.get("/create")
async def create_item(repository=Depends(item_repository)):  # type: ignore
    return await repository.create()
