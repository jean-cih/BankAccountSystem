from fastapi import APIRouter, Depends
from app.schemas import UserRequest, UserResponse
from app.service import users as users_service
from sqlalchemy.orm import Session
from app.dependency import get_db

router = APIRouter()

@router.post("/users", response_model=UserResponse)
def create_user(payload: UserRequest, db: Session = Depends(get_db)):
    return users_service.create_user(db, payload.login)

# @router.get("/users/me", response_model=UserResponse):
# def get_current_user()