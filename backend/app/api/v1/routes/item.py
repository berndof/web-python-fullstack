from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_item_repository

router = APIRouter(prefix="/item", tags=["item"])


@router.get("/")
async def get_items(repository=Depends(get_item_repository)):  # type: ignore
    return await repository.get_all()


@router.get("/create")
async def create_item(repository=Depends(get_item_repository)):  # type: ignore
    return await repository.create()
