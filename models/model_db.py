<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, Float, Boolean
from fastapi_users.db import SQLAlchemyBaseUserTable
from database import Base
from pydantic import BaseModel, ConfigDict


class DBUser(SQLAlchemyBaseUserTable[int], Base):  # Use int for ID (matches your setup)
=======
# models/model_db.py (updated: start_date default in code, kept unique on user_id for one sub per user)
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# SQLAlchemy ORM Models
class DBUser(Base):
>>>>>>> test
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    disabled: Mapped[bool] = mapped_column(Boolean, default=True)  # Unverified by default
    role: Mapped[str] = mapped_column(String, default="user")  # 'user' or 'admin'

<<<<<<< HEAD
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(100), nullable=True)
    disabled = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)  # New for verification
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

def __repr__(self):
        return f"<DBUser(id={self.id}, username='{self.username}', email='{self.email}')>"
=======
class Subscription(Base):
    __tablename__ = "subscriptions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)  # Unique per user
    plan: Mapped[str] = mapped_column(String, default="free")  # e.g., 'free', 'premium'
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  # NEW: Default in model
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String, default="active")  # 'active', 'expired', 'cancelled'
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)  # Soft delete
>>>>>>> test

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

<<<<<<< HEAD
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    gender = Column(String(50))
    height_cm = Column(Float)
    weight_kg = Column(Float)
    region = Column(String(100))
    area = Column(String(100))
    condition = Column(String(100))
    income_lpa = Column(Float)
    smoker = Column(Boolean)
    occupation = Column(String(50))
    user_id = Column(Integer)  # Link to user if needed


=======
# Pydantic Schemas
class RegisterInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
>>>>>>> test

class UserOut(BaseModel):
    id: int
    username: str
<<<<<<< HEAD
    email: str

    class Config:
        #orm_mode = True  # Use this for Pydantic v1; for v2, change to model_config = {"from_attributes": True}
        model_config = ConfigDict(from_attributes=True)








=======
    email: EmailStr
    full_name: str | None = None
    disabled: bool
    role: str
    model_config = {"from_attributes": True}
>>>>>>> test

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



    