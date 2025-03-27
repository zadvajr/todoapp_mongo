from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from crud.todo import todo_crud
from schemas import todo as todo_schema
from uuid import UUID

router = APIRouter(prefix="/todo", tags=["Todos"])

