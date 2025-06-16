from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import List
from .models import User, UserCreate, Token, UserInDB
from .utils import (
    verify_password, get_password_hash, create_access_token,
    load_users, save_users, ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    users_data = load_users()
    user = next((u for u in users_data["users"] if u["username"] == token_data.username), None)
    if user is None:
        raise credentials_exception
    return User(**user)

async def get_current_active_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    users_data = load_users()
    user = next((u for u in users_data["users"] if u["username"] == form_data.username), None)
    
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    user["last_login"] = datetime.utcnow().isoformat()
    save_users(users_data)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users", response_model=User)
async def create_user(
    user: UserCreate,
    current_user: User = Depends(get_current_active_admin)
):
    users_data = load_users()
    
    # Check if username already exists
    if any(u["username"] == user.username for u in users_data["users"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new user
    new_user = {
        "username": user.username,
        "password_hash": get_password_hash(user.password),
        "role": user.role,
        "created_at": datetime.utcnow().isoformat(),
        "last_login": None,
        "is_active": True
    }
    
    users_data["users"].append(new_user)
    save_users(users_data)
    
    return User(**new_user)

@router.get("/users", response_model=List[User])
async def get_users(current_user: User = Depends(get_current_active_admin)):
    users_data = load_users()
    return [User(**user) for user in users_data["users"]]

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user 