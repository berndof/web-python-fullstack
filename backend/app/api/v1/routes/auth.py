from fastapi import APIRouter
from app.schemas import UserLogin, Token


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
    async def login(user_in: UserLogin, service: AuthService = Depends(auth_service)):
        ...
