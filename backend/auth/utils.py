from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from .models import TokenData
import json
import os
from pathlib import Path

# Security
SECRET_KEY = "your-secret-key-here"  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_users_file_path() -> Path:
    return Path("users.json")

def load_users():
    users_file = get_users_file_path()
    if not users_file.exists():
        # Create default admin user
        default_admin = {
            "users": [{
                "username": "admin",
                "password_hash": get_password_hash("admin123"),  # Change this in production
                "role": "admin",
                "created_at": datetime.utcnow().isoformat(),
                "last_login": None,
                "is_active": True
            }]
        }
        with open(users_file, "w") as f:
            json.dump(default_admin, f, indent=2)
        return default_admin
    
    with open(users_file, "r") as f:
        return json.load(f)

def save_users(users_data: dict):
    with open(get_users_file_path(), "w") as f:
        json.dump(users_data, f, indent=2) 