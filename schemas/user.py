from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class User(UserBase):
    id: str
    created_at: datetime | str = datetime.now()

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass
