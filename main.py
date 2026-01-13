
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

from jose import jwt, JWTError  # ✅ Correct import for JWT

from config.region_tier import areas, regions  # Assuming these are sets/lists

# to get a string like this run: openssl rand -hex 32
SECRET_KEY = "9b1e82e5ba5870777e72d844869326c695f5c55edc9c18555594a65d681fe476"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "barakadaudi": {
        "username": "barakadaudi",
        "full_name": "Baraka Daudi",
        "email": "barakadaudi@example.com",
        "hashed_password": "$2b$12$4kdnL7GH3s8DvFA/dtJa7enqvsCNJ1ZupE6Tl4h39K2nt8BG0SmQ.",  # bcrypt hash for 'secret' (example)
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

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:  # ✅ Correct exception
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

app = FastAPI(title="Patient Management & Premium Predictor API")

# Expanded CORS for local + deployed (add your Streamlit cloud URL when deployed)
origins = [
    "http://localhost", "http://localhost:8000", "http://localhost:8501",
    "http://127.0.0.1:8000", "http://127.0.0.1:8501",
    "*"  # For testing; restrict in production
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single root endpoint
@app.get("/")
def root():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage patient records and predict insurance premiums"}

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Patient ID", examples=["P001"])]
    age: Annotated[int, Field(gt=0, lt=120)]
    gender: Annotated[str, Field(description="Gender")]
    height_cm: Annotated[float, Field(gt=0, lt=250, description="Height in cm")]
    weight_kg: Annotated[float, Field(gt=0, description="Weight in kg")]
    region: Annotated[str, Field(description="Region")]
    area: Annotated[str, Field(description="Area")]
    condition: Annotated[str, Field(description="Medical condition")]
    income_lpa: Annotated[float, Field(gt=0, description="Income in LPA")]
    smoker: Annotated[bool, Field(description="Smoker?")]
    occupation: Annotated[
        Literal["retired", "freelancer", "student", "government_job", "business_owner", "unemployed", "private_job"],
        Field(description="Occupation")
    ]

    @field_validator("region", "area", mode="before")
    @classmethod
    def normalize(cls, v: str) -> str:
        return v.strip().title()

    @computed_field
    @property
    def bmi(self) -> float:
        height_m = self.height_cm / 100
        return round(self.weight_kg / (height_m ** 2), 2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25: return "young"
        elif self.age < 45: return "adult"
        elif self.age < 60: return "middle_aged"
        return "senior"

    @computed_field
    @property
    def region_tier(self) -> int:
        if self.region in regions:
            return 1
        elif self.area in areas:
            return 2
        return 3

class PatientUpdate(BaseModel):
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender: Annotated[Optional[str], Field(default=None)]
    height_cm: Annotated[Optional[float], Field(default=None, gt=0, lt=250)]
    weight_kg: Annotated[Optional[float], Field(default=None, gt=0)]
    region: Annotated[Optional[str], Field(default=None)]  # Fixed: singular
    area: Annotated[Optional[str], Field(default=None)]    # Fixed: singular
    condition: Annotated[Optional[str], Field(default=None)]
    income_lpa: Annotated[Optional[float], Field(default=None, gt=0)]
    smoker: Annotated[Optional[bool], Field(default=None)]
    occupation: Annotated[
        Optional[Literal["retired", "freelancer", "student", "government_job", "business_owner", "unemployed", "private_job"]],
        Field(default=None)
    ]

def load_data() -> dict:
    try:
        with open('patients.json', 'r') as f:
            raw = json.load(f)
        if isinstance(raw, list):
            data = {}
            for item in raw:
                pid = item.pop("id", None)
                if pid:
                    data[pid] = Patient(id=pid, **item).model_dump(exclude=["id"])
            return data
        else:
            # Validate each entry
            return {k: Patient(id=k, **v).model_dump(exclude=["id"]) for k, v in raw.items()}
    except (FileNotFoundError, json.JSONDecodeError, Exception):
        return {}

def save_data(data: dict):
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=2)

@app.get("/view")
def view_all(current_user: Annotated[User, Depends(get_current_active_user)]):
    return load_data()

@app.get("/patient/{id}")
def view_patient(current_user: Annotated[User, Depends(get_current_active_user)], id: str = Path(..., examples=["P001"])):
    data = load_data()
    if id in data:
        return data[id]
    raise HTTPException(404, "Patient not found")

@app.get("/sort")
def sort_patients(current_user: Annotated[User, Depends(get_current_active_user)], sort_by: str = Query(..., description="height_cm, weight_kg, or bmi"),
                  order: str = Query("asc", description="asc or desc")):
    valid = ["height_cm", "weight_kg", "bmi"]
    if sort_by not in valid:
        raise HTTPException(400, f"Invalid field; choose from {valid}")
    if order not in ["asc", "desc"]:
        raise HTTPException(400, "Order must be asc or desc")
    data = load_data().values()
    sorted_data = sorted(data, key=lambda x: x.get(sort_by, 0), reverse=(order == "desc"))
    return sorted_data

@app.post("/create")
def create(patient: Patient, current_user: Annotated[User, Depends(get_current_active_user)]):
    data = load_data()
    if patient.id in data:
        raise HTTPException(400, "Patient already exists")
    data[patient.id] = patient.model_dump(exclude=["id"])
    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Patient created"})

@app.put("/edit/{patient_id}")
def update(patient_id: str, update: PatientUpdate, current_user: Annotated[User, Depends(get_current_active_user)]):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(404, "Patient not found")
    existing = data[patient_id]
    updates = update.model_dump(exclude_unset=True)
    existing.update(updates)
    # Re-validate to recompute fields
    try:
        validated = Patient(id=patient_id, **existing)
        data[patient_id] = validated.model_dump(exclude=["id"])
        save_data(data)
        return {"message": "Patient updated"}
    except ValueError as e:
        raise HTTPException(400, str(e))

@app.delete("/delete/{patient_id}")
def delete(patient_id: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(404, "Patient not found")
    del data[patient_id]
    save_data(data)
    return {"message": "Patient deleted"}

class PredictionInput(BaseModel):
    age: int
    gender: str  # ✅ Added
    height_cm: float  # ✅ Renamed/expected in cm
    weight_kg: float  # ✅ Renamed
    income_lpa: float  # ✅ Renamed
    smoker: bool
    condition: str  # ✅ Added
    region: str
    area: str
    occupation: str

@app.post("/predict")
def predict(data: PredictionInput):
    # TODO: Replace with real ML model
    # For dummy: Incorporate new fields (e.g., adjust risk if condition != "none" or gender-based factors)
    height_m = data.height_cm / 100
    bmi = data.weight_kg / (height_m ** 2)
    base_risk = "high" if data.smoker and bmi > 30 else "medium" if data.smoker or bmi > 27 else "low"
    # Simple adjustment examples:
    if data.condition != "none":
        base_risk = "high" if base_risk == "medium" else base_risk  # Escalate if pre-existing
    if data.gender == "male" and data.age > 50:  # Hypothetical gender/age factor
        base_risk = "medium" if base_risk == "low" else base_risk
    premium = base_risk.title()
    return {"premium_category": premium, "input_received": data.dict()}

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
















