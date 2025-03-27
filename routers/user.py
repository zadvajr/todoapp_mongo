from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId
from crud.user import user_crud
from schemas import user as user_schema

router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/", response_model=user_schema.UserCreate)
def create_user_endpoint(user: user_schema.UserCreate):
    return user_crud.create_user(user)

@router.get("/{user_id}", response_model=user_schema.UserCreate)
def get_user_endpoint(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid User ID format")

    user = user_crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/", response_model=list[user_schema.UserCreate])
def list_users_endpoint():
    return user_crud.list_users()

@router.delete("/{user_id}")
def delete_user_endpoint(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid User ID format")

    if not user_crud.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}