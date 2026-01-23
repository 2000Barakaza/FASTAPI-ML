# models/model_db.py (updated: consistent disabled, removed duplicates, added ForeignKey)
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from pydantic import BaseModel, EmailStr, Field

# SQLAlchemy ORM Models
class DBUser(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    disabled: Mapped[bool] = mapped_column(Boolean, default=True)  # Unverified by default

class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(50))
    height_cm: Mapped[float] = mapped_column(Float)
    weight_kg: Mapped[float] = mapped_column(Float)
    region: Mapped[str] = mapped_column(String(100))
    area: Mapped[str] = mapped_column(String(100))
    condition: Mapped[str] = mapped_column(String(100))
    income_lpa: Mapped[float] = mapped_column(Float)
    smoker: Mapped[bool] = mapped_column(Boolean)
    occupation: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

# Pydantic Schemas (no misleading defaults)
class RegisterInput(BaseModel):  # Single source of truth for registration
    email: EmailStr
    password: str = Field(min_length=8)

class UserOut(BaseModel):  # Public-facing user info
    id: int
    username: str
    email: EmailStr
    full_name: str | None = None
    disabled: bool  # Reflects actual state (no default override)
    model_config = {"from_attributes": True}

class UserMe(BaseModel):  # For /users/me (same as UserOut, or customize if needed)
    id: int
    username: str
    email: EmailStr
    full_name: str | None = None
    disabled: bool
    model_config = {"from_attributes": True}









    
