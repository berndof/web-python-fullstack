import uuid
from datetime import datetime

from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    fist_name: str
    last_name: str


class UserResponse(BaseUser):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
