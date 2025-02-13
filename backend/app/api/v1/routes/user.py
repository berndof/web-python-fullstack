from fastapi import APIRouter, Depends

from app.api.v1.dependencies import user_service
from app.schemas import UserCreate, UserResponse
from app.services import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/create", response_model=UserResponse)
async def create_user(user_in: UserCreate, service: UserService = Depends(user_service)):
    return await service.create(user_in)
