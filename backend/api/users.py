from fastapi import APIRouter, HTTPException, status, Depends, Header, Query
from typing import List
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from api.dependencies import get_db
from crud.user_crud import create_user,update_user,delete_user,get_users,greet_user
from schemas.user_schema import UserCreate, UserUpdate, UserResponse

router = APIRouter()

# Endpoint do tworzenia nowego użytkownika
@router.post("/", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db=db, user_data=user)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint do aktualizacji istniejącego użytkownika na podstawie jego ID
@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_current_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        updated_user = update_user(db=db, user_id=user_id,user_data=user)
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint do usunięcia użytkownika na podstawie jego ID
@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        delete_user(db=db, user_id=user_id)
        return JSONResponse(content={"message": "Successfully deleted user"}, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Endpoint do powitania użytkownika po ID
@router.get("/{user_id}/greet")
def greet_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        message = greet_user(db=db, user_id=user_id)
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

# endpoint pomocniczy:
@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = Query(0, ge=0), limit: int = Query(100, le=1000), db: Session = Depends(get_db)):
    users = get_users(db=db, skip=skip, limit=limit)
    return users