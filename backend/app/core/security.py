from passlib.context import CryptContext

C = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(plain_password: str) -> str:
    return C.hash(plain_password)

def validate_password(plain_password: str, hashed_password: str) -> bool:
    return C.verify(plain_password, hashed_password)