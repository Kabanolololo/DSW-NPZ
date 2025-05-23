from pydantic import BaseModel, EmailStr

# Schemat do logowania użytkownika
class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

# Schemat odpowiedzi zawierającej token uwierzytelniający
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True

# Schemat do wyswietelnia danych podczas logowania        
class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str

    class Config:
            from_attributes = True 