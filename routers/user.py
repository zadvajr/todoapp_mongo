from fastapi import APIRouter
from crud.user import user_crud
from schemas import user as user_schema

router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/")
def create_user_endpoint(user: user_schema.UserCreate):
    return user_crud.create_user(user)

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from models import UserCreate, UserRead
from crud.user import user_crud
from uuid import UUID

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserRead)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_session)):
    return user_crud.create_user(db, user)

@router.get("/{user_id}", response_model=UserRead)
def get_user_endpoint(user_id: UUID, db: Session = Depends(get_session)):
    user = user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    return user

@router.get("/", response_model=list[UserRead])
def list_users_endpoint(db: Session = Depends(get_session)):
    return user_crud.list_users(db)

@router.delete("/{user_id}")
def delete_user_endpoint(user_id: UUID, db: Session = Depends(get_session)):
    if not user_crud.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found!")
    return {"message": "User deleted successfully!"}

