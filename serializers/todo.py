from bson import ObjectId

def todo_serializer(todo) -> dict:
    return {
        "id": str(todo["_id"]),  # Convert ObjectId to string
        "user_id": todo["user_id"],
        "title": todo["title"],
        "description": todo["description"],
        "is_completed": todo["is_completed"]
    }

def todos_serializer(todos) -> list:
    return [todo_serializer(todo) for todo in todos]
