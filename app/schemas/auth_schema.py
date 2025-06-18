from enum import Enum
from pydantic import BaseModel, EmailStr, Field

class TokenType(str, Enum):
    ACCESS = 'ACCESS_TOKEN'

class UserBase(BaseModel):
    email: EmailStr = Field(..., examples=["usuario@ejemplo.com"])
    username: str = Field(..., min_length=3, max_length=50, examples=["usuario123"])
    password: str = Field(..., min_length=8, examples=["password123"])

class UserCreate(UserBase):
    pass
    

class UserLogin(BaseModel):
    email: EmailStr = Field(..., examples=["usuario@ejemplo.com"])
    password: str = Field(..., examples=["password123"])

