from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from serializers import user as serializer
from schemas.user import UserCreate
from database import user_collection

class UserCrud:

    @staticmethod
    def create_user(user: UserCreate):
        """Creates a new user in MongoDB."""
        user_data = jsonable_encoder(user)
        user_document_data = user_collection.insert_one(user_data)
        user_id = user_document_data.inserted_id
        user = user_collection.find_one({"_id": ObjectId(user_id)})

        if not user:
            raise HTTPException(status_code=500, detail="Failed to create user")

        return serializer.user_serializer(user)

    @staticmethod
    def get_user(user_id: str):
        """Fetches a user by ID from MongoDB."""
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid User ID format")

        user = user_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User with ID does not exist")

        return serializer.user_serializer(user)

    @staticmethod
    def list_users():
        """Fetches all users from MongoDB."""
        users = list(user_collection.find())
        return serializer.users_serializer(users)

    @staticmethod
    def update_user(user_id: str, user_data: UserCreate):
        """Updates a user in MongoDB."""
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid User ID format")

        db_user = user_collection.find_one({"_id": ObjectId(user_id)})
        if not db_user:
            raise HTTPException(status_code=404, detail="User with ID does not exist")

        update_data = jsonable_encoder(user_data.dict() if hasattr(user_data, "dict") else user_data.model_dump())

        updated_user = user_collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )

        if not updated_user:
            raise HTTPException(status_code=500, detail="Failed to update user")

        return serializer.user_serializer(updated_user)

    @staticmethod
    def delete_user(user_id: str):
        """Deletes a user from MongoDB."""
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid User ID format")

        user = user_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User with ID does not exist")

        deleted_user = user_collection.delete_one({"_id": ObjectId(user_id)})
        if deleted_user.deleted_count == 0:
            raise HTTPException(status_code=500, detail="Failed to delete user")

        return {"message": "User deleted successfully"}

user_crud = UserCrud()