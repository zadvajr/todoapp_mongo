from fastapi import HTTPException
from serializers.todo import todo_serializer, todos_serializer
from serializers import todo as serializer
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from schemas.todo import TodoCreate, Todo
from database import todo_collection
from pymongo import ReturnDocument

class TodoCrud:

    @staticmethod
    def create_todo(todo: TodoCreate):
        todo_data = jsonable_encoder(todo)
        todo_document_data = todo_collection.insert_one(todo_data)
        todo_id = todo_document_data.inserted_id
        todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
        return serializer.todo_serializer(todo)
    
    @staticmethod
    def get_todo(todo_id: str):
        todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
        if not todo:
            raise HTTPException(status_code=404, detail="Todo with ID does not exist")
        todo["id"] = str(todo.pop("_id"))
        return todo
    
    @staticmethod
    def list_todos():
        todos = list(todo_collection.find())
        return todos_serializer(todos)
    
    @staticmethod
    def update_todo(todo_id: str, todo_data: TodoCreate):
        try:
            object_id = ObjectId(todo_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid todo ID format")

        updated_todo = todo_collection.find_one_and_update(
            {"_id": object_id},
            {"$set": {k: v for k, v in todo_data.model_dump().items() if v is not None}},
            return_document=ReturnDocument.AFTER
        )

        if not updated_todo:
            raise HTTPException(status_code=404, detail="Todo with ID does not exist or update failed")

        return updated_todo
    
    @staticmethod
    def delete_todo(todo_id: str):
        todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
        if not todo:
            raise HTTPException(status_code=404, detail="Todo with ID does not exist")

        deleted_todo = todo_collection.delete_one({"_id": ObjectId(todo_id)})
        if deleted_todo.deleted_count == 0:
            raise HTTPException(status_code=500, detail="Failed to delete todo")

        return {"message": "Todo deleted successfully"}

    @staticmethod
    def list_todos_by_user(user_id: str):
        return list(todo_collection.find({"owner_id": user_id}))

todo_crud = TodoCrud()
