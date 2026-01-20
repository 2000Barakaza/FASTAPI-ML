from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base
from pydantic import BaseModel

class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(100), nullable=True)
    disabled = Column(Boolean, default=False)
def __repr__(self):
        return f"<DBUser(id={self.id}, username='{self.username}', email='{self.email}')>"


class Patient(Base):
    __tablename__ = "patients"

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

    
from pydantic import BaseModel

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True  # Use this for Pydantic v1; for v2, change to model_config = {"from_attributes": True}






