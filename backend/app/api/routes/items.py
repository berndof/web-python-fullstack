from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/")
def get_items():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]
