
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










from datetime import datetime, timedelta, timezone
from typing import Annotated, Literal, Optional
import json
from fastapi import Depends, FastAPI, HTTPException, Path, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel, Field, computed_field, field_validator
from jose import jwt, JWTError
from config.region_tier import areas, regions  # Assuming you have this file

# JWT config
SECRET_KEY = "9b1e82e5ba5870777e72d844869326c695f5c55edc9c18555594a65d681fe476"  # Change in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Fake DB (replace with real DB in production)
fake_users_db = {
    "barakadaudi": {
        "username": "barakadaudi",
        "full_name": "Baraka Daudi",
        "email": "barakadaudi@example.com",
        "hashed_password": "$2b$12$4kdnL7GH3s8DvFA/dtJaTenqvsCNJ1ZupE6Tl4h39K2nt8BG0SmQ.",  # bcrypt for 'secret'
        "disabled": False,
    }
}

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

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, identifier: str):
    # Check by username first
    if identifier in db:
        return UserInDB(**db[identifier])
    # Then by email
    for user_dict in db.values():
        if user_dict.get("email") == identifier:
            return UserInDB(**user_dict)
    return None

def authenticate_user(db, identifier: str, password: str):
    user = get_user(db, identifier)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

app = FastAPI(title="Insurance Premium Predictor API")

origins = ["*", "http://localhost", "http://localhost:8501", "http://127.0.0.1:8501"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def root():
    return {"message": "Insurance Premium Predictor API"}

@app.get("/about")
def about():
    return {"message": "Predict insurance premium categories"}

# ======================
# Authentication Routes
# ======================

@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username/email or password")
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return Token(access_token=access_token, token_type="bearer")

@app.post("/auth/register")
def register(email: str, password: str):
    # Check if email already exists
    if any(u["email"] == email for u in fake_users_db.values()):
        raise HTTPException(400, "Email already registered")
    
    # Generate username from email (e.g., barakadaudi from barakadaudi@example.com)
    username = email.split("@")[0].lower()
    if username in fake_users_db:
        raise HTTPException(400, "Username conflict; try a different email")
    
    hashed_password = get_password_hash(password)
    fake_users_db[username] = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password,
        "full_name": None,
        "disabled": False,
    }
    return JSONResponse(status_code=201, content={"message": "User registered successfully"})

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

# ======================
# Prediction Model
# ======================

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
def predict(data: PredictionInput, current_user: Annotated[User, Depends(get_current_active_user)]):
    # Dummy logic (replace with your ML model)
    height_m = data.height_cm / 100
    bmi = data.weight_kg / (height_m ** 2) if height_m > 0 else 0
    risk = "high" if (data.smoker and bmi > 30) or data.condition != "none" else \
           "medium" if data.smoker or bmi > 27 else "low"
    premium_category = risk.title()
    return {
        "premium_category": premium_category,
        "bmi": round(bmi, 2),
        "input_received": data.model_dump()
    }

# (Optional: Keep your patient management endpoints if needed, but commented out here for brevity)











