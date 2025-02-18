from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.dependencies import auth_service, get_current_user
from app.models import User
from app.schemas import Token, UserResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(auth_service)
):
    user = await service.authenticate_user(form_data.username, form_data.password)

    # Changing expire delta
    # access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = auth_service.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    access_token = service.create_access_token(data={"sub": user.username})
    print(access_token)

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
