from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from models.user import User
from api.dependencies import get_db
from typing import Optional
from datetime import datetime, timedelta
import random
import string

# Stałe JWT
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

# Tworzenie tokenu
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    nonce = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    to_encode.update({"exp": expire, "nonce": nonce})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Pobieranie użytkownika na podstawie tokenu
def get_current_user(
    token: str = Query(..., description="JWT token w query stringu"),
    db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Nieprawidłowy token")

        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Użytkownik nie znaleziony")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Nieprawidłowy token")
