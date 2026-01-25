
#from fastapi import FastAPI, Path, HTTPException, Query
#from fastapi.responses import JSONResponse
#from pydantic import BaseModel, Field, computed_field, field_validator
#from typing import Annotated, Literal, Optional
#from config.region_tier import regions, areas
#import json
#from fastapi.middleware.cors import CORSMiddleware

#app = FastAPI()


#origins = [
#    "http://localhost.tiangolo.com",
#    "https://localhost.tiangolo.com",
#    "http://localhost",
#    "http://localhost:8080",
#]
#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=origins,
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#)


#@app.get("/")
#async def main():
#    return {"message": "Hello World"}


#class Patient(BaseModel):
#   id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
#    age: Annotated[int, Field(gt=0, lt=120, description="Age of the user")]
#    gender: Annotated[str, Field(description="Gender of the user")]
#    height_cm: Annotated[float, Field(gt=0, lt=250, description="Height in cm")]
#   weight_kg: Annotated[float, Field(gt=0, description="Weight in kg")]
#   region: Annotated[str, Field(description="Region")]
#   area: Annotated[str, Field(description="Area")]
#   condition: Annotated[str, Field(description="Medical condition")]
#   income_lpa: Annotated[float, Field(gt=0, description="Income in LPA")]
#   smoker: Annotated[bool, Field(description="Is smoker")]
#    occupation: Annotated[
#        Literal[
#            "retired",
#            "freelancer",
#            "student",
#            "government_job",
#            "business_owner",
#            "unemployed",
#           "private_job",
#        ],
#        Field(description="Occupation"),
#    ]

    # ======================
    # Validators
    # ======================
#    @field_validator("region")
#    def normalize_regions(cls, v: str) -> str:
#        return v.strip().title()

#    @field_validator("area")
#    def normalize_areas(cls, v: str) -> str:
#        return v.strip().title()

    # ======================
    # Computed fields
    # ======================
#    @property
#    def bmi(self) -> float:
#        height_m = self.height_cm / 100
#        return round(self.weight_kg / (height_m ** 2), 2)

#    @property
#    def lifestyle_risk(self) -> str:
#        if self.smoker and self.bmi > 30:
#            return "high"
#        elif self.smoker or self.bmi > 27:
#            return "medium"
#        return "low"

#    @property
#    def age_group(self) -> str:
#        if self.age < 25:
#            return "young"
#        elif self.age < 45:
#            return "adult"
#        elif self.age < 60:
#            return "middle_aged"
#        return "senior"

#    @property
#    @property
#    def region_tier(self) -> int:
#        if self.regions in regions:
#            return 1
#        elif self.areas in areas:
#            return 2
#        return 3

#class PatientUpdate(BaseModel):
#    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
#    gender: Annotated[Optional[str], Field(default=None)]
#    height_cm: Annotated[Optional[float], Field(default=None, gt=0, lt=250)]
#    weight_kg: Annotated[Optional[float], Field(default=None, gt=0)]
#    regions: Annotated[Optional[str], Field(default=None)]
#    areas: Annotated[Optional[str], Field(default=None)]
#    condition: Annotated[Optional[str], Field(default=None)]
#    income_lpa: Annotated[Optional[float], Field(default=None, gt=0)]
#    smoker: Annotated[Optional[bool], Field(default=None)]
#    occupation: Annotated[
#        Optional[Literal[
#            "retired",
#            "freelancer",
#            "student",
#            "government_job",
#            "business_owner",
#            "unemployed",
#            "private_job",
#        ]],
#        Field(default=None),
#    ]

#def load_data():
#    try:
#        with open('patients.json', 'r') as f:
#            data = json.load(f)
#        if isinstance(data, list):
#            return {p["id"]: p for p in data}
#        return data
#    except FileNotFoundError:
#        return {}

#def save_data(data):
#    with open('patients.json', 'w') as f:
#        json.dump(data, f)

#@app.get("/")
#def hello():
#    return {'message':'Patient Management System API'}

#@app.get('/about')
#def about():
#    return {'message': 'A fully functional API to manage your patient records'}

#@app.get('/view')
#def view():
#    data = load_data()
#    return data

#@app.get('/patient/{id}')
#def view_patient(id: str = Path(..., description='ID of the patient in the DB', examples=['P001'])):
#    data = load_data()
#    if id in data:
#        return data[id]
#    raise HTTPException(status_code=404, detail='Patient not found')
#@app.get('/sort')
#def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height_cm, weight_kg or bmi'), order: str = Query('asc', description='sort in asc or desc order')):
#    valid_fields = ['height_cm', 'weight_kg', 'bmi']
#    if sort_by not in valid_fields:
#        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
#    if order not in ['asc', 'desc']:
#        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
#    data = load_data()
#    sort_order = True if order == 'desc' else False
#    sorted_data = sorted(
#        data.values(),
#        key=lambda x: x.get(sort_by, 0),
#        reverse=sort_order
#    )
#    return sorted_data

#@app.post('/create')
#def create_patient(patient: Patient):
#    data = load_data()
#    if patient.id in data:
#        raise HTTPException(status_code=400, detail='Patient already exists')
#    data[patient.id] = patient.model_dump(exclude=['id'])
#    save_data(data)
#    return JSONResponse(status_code=201, content={'message':'patient created successfully'})

#@app.put('/edit/{patient_id}')
#def update_patient(patient_id: str, patient_update: PatientUpdate):
#    data = load_data()
#    if patient_id not in data:
#        raise HTTPException(status_code=404, detail='Patient not found')
#    existing_patient_info = data[patient_id]
#    updated_patient_info = patient_update.model_dump(exclude_unset=True)
#    for key, value in updated_patient_info.items():
#        existing_patient_info[key] = value
#    existing_patient_info['id'] = patient_id
#    patient_pydantic_obj = Patient(**existing_patient_info)
#    existing_patient_info = patient_pydantic_obj.model_dump(exclude=['id'])
#    data[patient_id] = existing_patient_info
#    save_data(data)
#    return JSONResponse(status_code=200, content={'message':'patient updated'})

#@app.delete('/delete/{patient_id}')
#def delete_patient(patient_id: str):
#    data = load_data()
#    if patient_id not in data:
#        raise HTTPException(status_code=404, detail='Patient not found')
#    del data[patient_id]
#    save_data(data)
#    return JSONResponse(status_code=200, content={'message':'patient deleted'})


#class PredictionInput(BaseModel):
#    age: int
#    weight: float
#    height: float
#    income: float
#    smoker: bool
#    region: str
#    area: str
#    occupation: str

#@app.post("/predict")
#def predict(data: PredictionInput):
#    # TEMP: replace with your real ML model
#    return {
#        "premium_category": "Medium",
#        "input_received": data
#    }






# main.py (updated: token creation now includes sub, no other changes)
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated
from fastapi_users import db
from models.model_db import UserOut
import os
from dotenv import load_dotenv
from app.auth import UserRead
# SQLAlchemy imports
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from datetime import datetime, timedelta
from database import engine, get_db, Base
from config.region_tier import areas, regions # Assuming you have this file
from email_service import send_email 
from models.model_db import RegisterInput
from app.auth import ( # Import only necessary items
    Token, User,RegisterInput,
    oauth2_scheme,
    get_current_user, get_current_active_user, get_current_admin,
    authenticate_user, create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_password_hash,verify_password
)
from models.model_db import DBUser, Subscription, Prediction, EmailVerification  # NEW: Import Subscription, Prediction
from uuid import uuid4
load_dotenv()
app = FastAPI(title=os.getenv("APP_TITLE", "Insurance Premium Predictor API"))
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Create tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
@app.get("/")
def root():
    return {"message": "Insurance Premium Predictor API"}
@app.get("/about")
def about():
    return {"message": "Predict insurance premium categories"}
@app.post(
    "/token",
    response_model=Token,
    responses={
        status.HTTP_200_OK: {"description": "Successful authentication"},
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication failed",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect username/email or password"}
                }
            },
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error (e.g., invalid grant_type)"
        },
    },
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if user == "not_verified":
      raise HTTPException(status_code=401, detail="Email not verified. Check your inbox.")
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username/email or password")
    access_token = create_access_token(
        data={
            "sub": str(user.id),  # FIXED: Add sub with user.id
            "uid": user.id  # Added for improvement
        },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=access_token, token_type="bearer")
@app.post(
    "/auth/register",
    #response_model=RegisterInput,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "User registered successfully"},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Email or username already registered",
            "content": {
                "application/json": {
                    "example": {"detail": "Email or username already registered"}
                }
            },
        },
    },
)
def register(
    register_input: RegisterInput,
    db: Session = Depends(get_db)
):
 
    # Normalize email
    email = register_input.email.strip().lower()
 
    # Check if email or username already exists in DB
    username_base = email.split("@")[0]
    username = f"{username_base}_{uuid4().hex[:6]}" # Unique username with UUID
    existing_user = db.query(DBUser).filter(
        or_(
            DBUser.email == email,
            DBUser.username == username
        )
    ).first()
    if existing_user:
        raise HTTPException(400, "Email or username already registered")
    hashed_password = get_password_hash(register_input.password)
    new_user = DBUser(
        username=username,
        email=email,
        hashed_password=hashed_password,
        full_name=None, # Can add later if needed
        disabled=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    verification_token = uuid4().hex
    expires_at = datetime.utcnow() + timedelta(hours=24)
    verification = EmailVerification(
        user_id=new_user.id,
        token=verification_token,
        expires_at=expires_at
    )
    db.add(verification)
    db.commit()
    db.refresh(verification)
    verification_link = f"{os.getenv('APP_URL')}/auth/verify-email?token={verification_token}"
    send_email(
        to_email=new_user.email,
        subject="Verify your email",
        html_content=f"""
            <h3>Welcome!</h3>
            <p>Click the link below to verify your email:</p>
            <a href="{verification_link}">Verify Email</a>
            <p>This link expires in 24 hours.</p>
        """
    )
    return JSONResponse(status_code=201, content={"message": "User registered successfully"})

@app.get("/auth/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    verification = db.query(EmailVerification).filter(
        EmailVerification.token == token,
        EmailVerification.used == False
    ).first()
    if not verification:
        raise HTTPException(400, "Invalid or expired token")
    if verification.expires_at < datetime.utcnow():
        raise HTTPException(400, "Token expired")
    user = db.query(DBUser).filter(DBUser.id == verification.user_id).first()
    user.is_verified = True
    verification.used = True
    db.commit()
    return {"message": "Email verified successfully"}

@app.get("/users/me/", response_model=UserOut)
async def read_users_me(current_user: Annotated[DBUser, Depends(get_current_active_user)]):
    return current_user
# Added: New endpoint to list all users
@app.get("/users", response_model=list[UserOut])
def get_users(admin: Annotated[DBUser, Depends(get_current_admin)], db: Session = Depends(get_db)):
    return db.query(DBUser).all()
class PredictionInput(BaseModel):
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    income_lpa: float
    smoker: bool
    condition: str
    region: str
    area: str
    occupation: str
@app.post("/predict")
def predict(
    data: PredictionInput,
    current_user: Annotated[DBUser, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    # NEW: Subscription check
    sub = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == "active",
        Subscription.is_deleted == False
    ).first()
    if not sub or sub.plan == "free":
        raise HTTPException(403, "Active premium subscription required for predictions")
   
    height_m = data.height_cm / 100
    bmi = data.weight_kg / (height_m ** 2) if height_m > 0 else 0
    risk = "high" if (data.smoker and bmi > 30) or data.condition != "none" else \
           "medium" if data.smoker or bmi > 27 else "low"
    premium_category = risk.title()
    # NEW: Save prediction history
    prediction = Prediction(user_id=current_user.id, risk=premium_category, bmi=bmi)
    db.add(prediction)
    db.commit()
    return {
        "premium_category": premium_category,
        "bmi": round(bmi, 2),
        "input_received": data.model_dump()
    }

# NEW: User's prediction history
@app.get("/predictions/me")
def get_my_predictions(
    current_user: Annotated[DBUser, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    predictions = db.query(Prediction).filter(Prediction.user_id == current_user.id)\
        .order_by(Prediction.created_at.desc()).all()
    return [
        {
            "created_at": p.created_at.isoformat(),
            "premium_category": p.risk,
            "bmi": p.bmi
        } for p in predictions
    ]


# NEW: Admin stats
@app.get("/admin/stats")
def admin_stats(
    admin: Annotated[DBUser, Depends(get_current_admin)],
    db: Session = Depends(get_db)
):
    total_users = db.query(DBUser).count()
    active_users = db.query(DBUser).filter(~DBUser.disabled).count()
    total_subscriptions = db.query(Subscription).filter(Subscription.is_deleted == False).count()
    active_subscriptions = db.query(Subscription).filter(
        Subscription.status == "active",
        Subscription.is_deleted == False
    ).count()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "subscriptions": total_subscriptions,
        "active_subscriptions": active_subscriptions
    }

# NEW: Daily prediction counts for admin chart
@app.get("/admin/predictions/daily")
def daily_predictions(
    admin: Annotated[DBUser, Depends(get_current_admin)],
    db: Session = Depends(get_db)
):
    daily = db.query(
        func.date(Prediction.created_at).label('date'),
        func.count(Prediction.id).label('count')
    ).group_by(func.date(Prediction.created_at))\
     .order_by('date').all()
    
    return [{"date": d.date.strftime("%Y-%m-%d"), "count": d.count} for d in daily]


@app.get("/test-email")
def test_email():
    status = send_email(
        to_email="your_other_email@gmail.com",
        subject="SendGrid works!",
        html_content="<h2>Your email setup is successful 🚀</h2>"
    )
    return {"status": status}


# NEW: Subscription routes
@app.get("/subscriptions/me")
def get_my_subscription(current_user: Annotated[DBUser, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.user_id == current_user.id).first()
    if not sub:
        return {"plan": "free", "status": "free"}
    return {
        "plan": sub.plan,
        "status": sub.status,
        "start_date": sub.start_date.isoformat(),
        "end_date": sub.end_date.isoformat() if sub.end_date else None
    }

class SubscriptionUpgrade(BaseModel):
    plan: str

@app.post("/subscriptions/upgrade")
def upgrade_subscription(
    request: SubscriptionUpgrade,
    current_user: Annotated[DBUser, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    if request.plan not in ["free", "premium"]:
        raise HTTPException(400, "Invalid plan")

    # FIXED: Filter out soft-deleted subscriptions
    sub = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.is_deleted == False
    ).first()

    if sub:
        # Update existing active subscription
        sub.plan = request.plan
        sub.status = "active" if request.plan == "premium" else "free"
        sub.start_date = datetime.utcnow()
        sub.end_date = datetime.utcnow() + timedelta(days=30) if request.plan == "premium" else None
    else:
        # Create new subscription (only if no active one exists)
        sub = Subscription(
            user_id=current_user.id,
            plan=request.plan,
            status="active" if request.plan == "premium" else "free",
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=30) if request.plan == "premium" else None,
            is_deleted=False
        )
        db.add(sub)

    db.commit()
    db.refresh(sub)

    # OPTIONAL: Debug print (remove in production)
    print(f"UPGRADE SUCCESS: User {current_user.id} -> Plan: {sub.plan}, Status: {sub.status}")

    return {
        "plan": sub.plan,
        "status": sub.status,
        "start_date": sub.start_date.isoformat(),
        "end_date": sub.end_date.isoformat() if sub.end_date else None
    }


@app.post("/subscribe")
def subscribe(
    plan: str,
    current_user: Annotated[DBUser, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    existing = db.query(Subscription).filter(Subscription.user_id == current_user.id).first()
    if existing:
        existing.plan = plan
        existing.status = "active"
        existing.start_date = datetime.utcnow()
        existing.end_date = None
    else:
        new_sub = Subscription(
            user_id=current_user.id,
            plan=plan,
            start_date=datetime.utcnow(),
            status="active"
        )
        db.add(new_sub)
    db.commit() 
    return {"message": "Subscribed successfully"}







##### user example email
## -------manjale2021@gmail.com
## 2------2000B1r1d1
















