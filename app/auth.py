# auth.py (fixed: added sub in token creation example, used db.get, updated tokenUrl)
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel, Field, EmailStr
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
from models.model_db import DBUser
import os
from dotenv import load_dotenv

load_dotenv()

# Critical: No fallback – SECRET_KEY must be in .env
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in .env – this is required for security!")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")  # FIXED: Proper tokenUrl

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserRead(BaseModel):
    id: int
    email: EmailStr
    disabled: bool
    model_config = {"from_attributes": True}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_by_login(identifier: str, db: Session) -> DBUser | None:
    return db.query(DBUser).filter(
        or_(DBUser.username == identifier, DBUser.email == identifier)
    ).first()

def authenticate_user(identifier: str, password: str, db: Session):
    user = get_user_by_login(identifier, db)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_email_token(token: str, db: Session) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "verify":
            return False
        email: str = payload.get("sub")
        if email is None:
            return False
        user = db.query(DBUser).filter(DBUser.email == email).first()
        if not user:
            return False
        if not user.disabled:
            return True # Already verified
        user.disabled = False
        db.commit()
        return True
    except JWTError:
        return False

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> DBUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.get(DBUser, int(user_id))  # FIXED: Use db.get
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[DBUser, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# NEW: Admin dependency
async def get_current_admin(current_user: Annotated[DBUser, Depends(get_current_active_user)]):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user






