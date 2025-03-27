def user_serializer(user_document) -> dict:
    return {
        "id": str(user_document.get("_id")),
        "username": user_document.get("username"),
        "created_at": user_document.get("created_at"),
    }

def users_serializer(users_documents) -> list:
    user_schema = []
    for user in users_documents:
        user_schema.append(user_serializer(user))
    return user_schema

