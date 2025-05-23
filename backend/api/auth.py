from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from schemas.auth_schema import UserLogin
from api.dependencies import get_db
from crud.auth_crud import login_user

router = APIRouter()

# Endpoint do logowania
@router.post("/login", status_code=status.HTTP_200_OK)
def login(user: UserLogin, db: Session = Depends(get_db)):
    result = login_user(db=db, user=user)
    return result

# Endpoint do wylogowania
# Usuwamy jwt po stronie uzytkownika - frontend