from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class UserBase(BaseModel):
    username: str

class User(UserBase):
    id: UUID
    created_at: datetime = datetime.now()

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass
