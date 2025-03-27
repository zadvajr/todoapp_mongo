from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId
from crud.todo import todo_crud
from schemas import todo as todo_schema
from serializers.todo import todos_serializer

router = APIRouter(prefix="/todo", tags=["Todos"])

@router.post("/", response_model=todo_schema.Todo)
def create_todo_endpoint(todo: todo_schema.TodoCreate):
    return todo_crud.create_todo(todo)

@router.get("/{todo_id}", response_model=todo_schema.Todo)
def get_todo_endpoint(todo_id: str):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="Invalid Todo ID format")
    
    todo = todo_crud.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return todo

@router.get("/", response_model=list[todo_schema.Todo])
def list_todos_endpoint():
    return todo_crud.list_todos()

@router.put("/{todo_id}", response_model=todo_schema.Todo)
def update_todo_endpoint(todo_id: str, todo: todo_schema.TodoCreate):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="Invalid Todo ID format")

    updated_todo = todo_crud.update_todo(todo_id, todo)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return updated_todo

@router.delete("/{todo_id}")
def delete_todo_endpoint(todo_id: str):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="Invalid Todo ID format")

    if not todo_crud.delete_todo(todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return {"message": "Todo deleted successfully"}

@router.get("/user/{user_id}", response_model=list[todo_schema.Todo])
def get_todos_for_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid User ID format")

    todos = todo_crud.list_todos_by_user(user_id)
    if not todos:
        raise HTTPException(status_code=404, detail="No Todos found for this user")
    
    return todos
