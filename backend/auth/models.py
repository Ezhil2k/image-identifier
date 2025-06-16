from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    role: str = "user"

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    password_hash: str
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True

class User(UserBase):
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None 