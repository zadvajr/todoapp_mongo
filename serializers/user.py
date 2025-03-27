def user_serializer(user_document) -> dict:
    return {
        "id": str(user_document.get("_id")),
        "username": user_document.get("username"),
        "created_at": user_document.get("created_at"),
    }