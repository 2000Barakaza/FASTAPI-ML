from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

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





    