from fastapi import APIRouter, Depends

from app.api.v1.dependencies import item_service

router = APIRouter(prefix="/item", tags=["item"])


@router.get("/get_all")
async def get_items(service=Depends(item_service)):  # type: ignore
    return await service.get_all()


@router.get("/create")
async def create_item(service=Depends(item_service)):  # type: ignore
    return await service.create()
