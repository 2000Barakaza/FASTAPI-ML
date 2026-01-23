# auth.py (updated: generic token creation, verify_email_token, consistent DBUser returns)
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
from models.model_db import DBUser
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in .env")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user(identifier: str, db: Session) -> DBUser | None:
    return db.query(DBUser).filter(
        or_(DBUser.username == identifier, DBUser.email == identifier)
    ).first()

def authenticate_user(identifier: str, password: str, db: Session) -> DBUser | None:
    user = get_user(identifier, db)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Email verification token validation
def verify_email_token(token: str, db: Session) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "verify":
            return False
        email: str | None = payload.get("sub")
        if not email:
            return False
        user = db.query(DBUser).filter(DBUser.email == email).first()
        if not user:
            return False
        if not user.disabled:
            return True  # Already verified
        user.disabled = False
        db.commit()
        return True
    except JWTError:
        return False

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
) -> DBUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username, db)
    if not user:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[DBUser, Depends(get_current_user)]
) -> DBUser:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user





