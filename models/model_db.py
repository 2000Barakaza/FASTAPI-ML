# models/model_db.py

from datetime import datetime
from sqlalchemy import String, Float, Boolean, ForeignKey, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from pydantic import BaseModel, EmailStr, Field


# =========================
# SQLAlchemy ORM Models
# =========================

class DBUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    disabled: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String(20), default="user")  # user | admin

    def __repr__(self) -> str:
        return f"<DBUser id={self.id} username={self.username}>"



class EmailVerification(Base):
    __tablename__ = "email_verification"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    token: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    used: Mapped[bool] = mapped_column(Boolean, default=False)



class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )

    plan: Mapped[str] = mapped_column(String(20), default="free")
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active")
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    risk: Mapped[str] = mapped_column(String(50))
    bmi: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)


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

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

# =========================
# Pydantic Schemas
# =========================

class RegisterInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str | None
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
    plan: str


class PredictionOut(BaseModel):
    id: int
    risk: str
    bmi: float
    created_at: datetime

    model_config = {"from_attributes": True}

    








