from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

C = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return C.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return C.verify(plain_password, hashed_password)
