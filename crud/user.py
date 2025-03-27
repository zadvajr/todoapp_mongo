from serializers import user as serializer
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from schemas.user import UserCreate
from database import user_collection

class UserCrud:

    @staticmethod
    def create_user(user: UserCreate):
        user_data = jsonable_encoder(user)
        user_document_data = user_collection.insert_one(user_data)
        user_id = user_document_data.inserted_id
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        return serializer.user_serializer(user)

user_crud = UserCrud()