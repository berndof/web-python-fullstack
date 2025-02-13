from fastapi import APIRouter

from app.api.v1.routes import item, user

v1_api_router = APIRouter(prefix="/v1")

v1_api_router.include_router(item.router)
v1_api_router.include_router(user.router)
