# auth.py (fixed: added sub in token creation example, used db.get, updated tokenUrl)
from datetime import datetime, timedelta, timezone
from typing import Annotated,Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel, Field, EmailStr
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
from fastapi import Request
#from fastapi_users.router import BaseUserManager
from fastapi_users.manager import BaseUserManager
from fastapi_users import models
from models.model_db import DBUser, EmailVerification   
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
    is_superuser: bool = False
    is_active: bool = True
    is_verified: bool = False


class UserRead(BaseModel):
    id: int
    email: EmailStr
    disabled: bool
    model_config = {"from_attributes": True}


class UserInDB(BaseModel):
    id: int
    username: str
    email: EmailStr
    disabled: bool = False
    model_config = {"from_attributes": True} # Handles ORM-to-dict conversion
class RegisterInput(BaseModel):
    email: str
    password: str = Field(min_length=8)


from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, EmailStr

from fastapi_users import models

SCHEMA = TypeVar("SCHEMA", bound=BaseModel)


class CreateUpdateDictModel(BaseModel):
    def create_update_dict(self):
        return self.model_dump(
            exclude_unset=True,
            exclude={
                "id",
                "is_superuser",
                "is_active",
                "is_verified",
                "oauth_accounts",
            },
        )

    def create_update_dict_superuser(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})


class BaseUser(CreateUpdateDictModel, Generic[models.ID]):
    """Base User model."""

    id: models.ID
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    model_config = ConfigDict(from_attributes=True)


class BaseUserCreate(CreateUpdateDictModel):
    email: EmailStr
    password: str
    is_active: bool | None = True
    is_superuser: bool | None = False
    is_verified: bool | None = False


class BaseUserUpdate(CreateUpdateDictModel):
    password: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    is_verified: bool | None = None


U = TypeVar("U", bound=BaseUser)
UC = TypeVar("UC", bound=BaseUserCreate)
UU = TypeVar("UU", bound=BaseUserUpdate)


class BaseOAuthAccount(BaseModel, Generic[models.ID]):
    """Base OAuth account model."""

    id: models.ID
    oauth_name: str
    access_token: str
    expires_at: int | None = None
    refresh_token: str | None = None
    account_id: str
    account_email: str

    model_config = ConfigDict(from_attributes=True)


class BaseOAuthAccountMixin(BaseModel):
    """Adds OAuth accounts list to a User model."""

    oauth_accounts: list[BaseOAuthAccount] = []

class UserManager(BaseUserManager[models.UP, DBUser]):
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY
    reset_password_token_lifetime_seconds = 3600
    verification_token_lifetime_seconds = 3600

    async def on_after_register(self, user: DBUser, request: Optional [Request] = None):
        print(f"User {user.id} registered. Requesting verification...")
        await self.request_verify(user)  # Auto-request verification after register

    async def on_after_request_verify(self, user: DBUser, token: str, request: Optional [Request] = None):
        # Send email with verification link
        verify_url = f"http://127.0.0.1:8000/auth/verify?token={token}"  # Adjust for prod
        html_content = f"<h2>Verify your email</h2><p>Click <a href='{verify_url}'>here</a> to verify. Expires in {3600 // 60} minutes.</p>"
        send_email(to_email=user.email, subject="Verify Your Account", html_content=html_content)
        print(f"Verification email sent to {user.email}. Token: {token}")


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












