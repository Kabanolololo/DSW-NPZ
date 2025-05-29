from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.auth_schema import UserLogin
from api.dependencies import get_db
from crud.auth_crud import login_user
from schemas.user_schema import UserCreate, UserResponse
from crud.user_crud import create_user
from models.user import User
from utils.jwt import get_current_user  # ← poprawna funkcja z Depends()

router = APIRouter()

# Endpoint do logowania
@router.post("/login", status_code=status.HTTP_200_OK)
def login(user: UserLogin, db: Session = Depends(get_db)):
    result = login_user(db=db, user=user)
    return result

# Endpoint do rejestracji
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db, user_data)
        return {"message": "User registered successfully", "user_id": new_user.id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Endpoint do pobrania profilu zalogowanego użytkownika
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user