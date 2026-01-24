# models/model_db.py (updated: start_date default in code, kept unique on user_id for one sub per user)
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# SQLAlchemy ORM Models
class DBUser(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    disabled: Mapped[bool] = mapped_column(Boolean, default=True)  # Unverified by default
    role: Mapped[str] = mapped_column(String, default="user")  # 'user' or 'admin'

class Subscription(Base):
    __tablename__ = "subscriptions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)  # Unique per user
    plan: Mapped[str] = mapped_column(String, default="free")  # e.g., 'free', 'premium'
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  # NEW: Default in model
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String, default="active")  # 'active', 'expired', 'cancelled'
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)  # Soft delete

class Prediction(Base):
    __tablename__ = "predictions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    risk: Mapped[str] = mapped_column(String)
    bmi: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)  # Soft delete

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

# Pydantic Schemas
class RegisterInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str | None = None
    disabled: bool
    role: str
    model_config = {"from_attributes": True}

class SubscriptionOut(BaseModel):
    id: int
    plan: str
    start_date: datetime
    end_date: datetime | None
    status: str
    model_config = {"from_attributes": True}

class SubscriptionCreate(BaseModel):
    plan: str  # e.g., "premium"

class PredictionOut(BaseModel):
    id: int
    risk: str
    bmi: float
    created_at: datetime
    model_config = {"from_attributes": True}



    