from fastapi import APIRouter
from crud.todo import todo_crud
from schemas import todo as todo_schema

router = APIRouter(prefix="/todo", tags=["Todos"])

@router.post("/", response_model=todo_schema.Todo)
def create_todo_endpoint(todo: todo_schema.TodoCreate):
    return todo_crud.create_todo(todo)