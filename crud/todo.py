from serializers import todo as serializer
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from schemas.todo import TodoCreate
from database import todo_collection

class TodoCrud:

    @staticmethod
    def create_todo(todo: TodoCreate):
        todo_data = jsonable_encoder(todo)
        todo_document_data = todo_collection.insert_one(todo_data)
        todo_id = todo_document_data.inserted_id
        todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
        return serializer.todo_serializer(todo)

todo_crud = TodoCrud()