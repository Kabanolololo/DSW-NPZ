from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True