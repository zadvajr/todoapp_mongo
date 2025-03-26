from uuid import UUID
from pydantic import BaseModel

class TodoBase(BaseModel):
    user_id: UUID
    title: str
    description: str
    is_completed: bool

class Todo(TodoBase):
    id: UUID

class TodoCreate(TodoBase):
    is_completed: bool = False
    pass
