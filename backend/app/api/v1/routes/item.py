from fastapi import APIRouter

router = APIRouter(prefix="/item", tags=["item"])


@router.get("/")
def get_items():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]
