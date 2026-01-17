
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




from fastapi import FastAPI, Path, HTTPException, Query, Depends, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated, Literal, Optional
from config.region_tier import regions, areas  # Assuming this file exists with lists/dicts
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext

# JWT config
SECRET_KEY = "9b1e82e5ba5870777e72d844869326c695f5c55edc9c18555594a65d681fe476"  # Change in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(title="Insurance Premium Predictor API")

# CORS setup (combined from both snippets)
origins = [
    "*",
    "http://localhost",
    "http://localhost:8501",
    "http://127.0.0.1:8501",
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MySQL connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Add your password here
        database="fastapi_ml"
    )

# ======================
# Authentication Helpers
# ======================
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

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(identifier: str):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # Check by username or email
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (identifier, identifier))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return UserInDB(**user) if user else None
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

def authenticate_user(identifier: str, password: str):
    user = get_user(identifier)
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
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# ======================
# Patient Models (from first snippet, with fixes)
# ======================
class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    age: Annotated[int, Field(gt=0, lt=120, description="Age of the user")]
    gender: Annotated[str, Field(description="Gender of the user")]
    height_cm: Annotated[float, Field(gt=0, lt=250, description="Height in cm")]
    weight_kg: Annotated[float, Field(gt=0, description="Weight in kg")]
    region: Annotated[str, Field(description="Region")]
    area: Annotated[str, Field(description="Area")]
    condition: Annotated[str, Field(description="Medical condition")]
    income_lpa: Annotated[float, Field(gt=0, description="Income in LPA")]
    smoker: Annotated[bool, Field(description="Is smoker")]
    occupation: Annotated[
        Literal[
            "retired",
            "freelancer",
            "student",
            "government_job",
            "business_owner",
            "unemployed",
            "private_job",
        ],
        Field(description="Occupation"),
    ]

    # Validators
    @field_validator("region")
    def normalize_regions(cls, v: str) -> str:
        return v.strip().title()

    @field_validator("area")
    def normalize_areas(cls, v: str) -> str:
        return v.strip().title()

    # Computed fields (added @computed_field for Pydantic v2)
    @computed_field
    @property
    def bmi(self) -> float:
        height_m = self.height_cm / 100
        return round(self.weight_kg / (height_m ** 2), 2) if height_m > 0 else 0.0

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
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    @computed_field
    @property
    def region_tier(self) -> int:
        if self.region in regions:  # Fixed: self.region (not self.regions)
            return 1
        elif self.area in areas:  # Fixed: self.area (not self.areas)
            return 2
        return 3

class PatientUpdate(BaseModel):
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender: Annotated[Optional[str], Field(default=None)]
    height_cm: Annotated[Optional[float], Field(default=None, gt=0, lt=250)]
    weight_kg: Annotated[Optional[float], Field(default=None, gt=0)]
    region: Annotated[Optional[str], Field(default=None)]
    area: Annotated[Optional[str], Field(default=None)]
    condition: Annotated[Optional[str], Field(default=None)]
    income_lpa: Annotated[Optional[float], Field(default=None, gt=0)]
    smoker: Annotated[Optional[bool], Field(default=None)]
    occupation: Annotated[
        Optional[Literal[
            "retired",
            "freelancer",
            "student",
            "government_job",
            "business_owner",
            "unemployed",
            "private_job",
        ]],
        Field(default=None),
    ]

# ======================
# Patient MySQL Helpers
# ======================
def get_patients():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_patient(patient_id: str):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_patient_in_db(patient: Patient):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO patients (id, age, gender, height_cm, weight_kg, region, area, condition, income_lpa, smoker, occupation)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            patient.id, patient.age, patient.gender, patient.height_cm, patient.weight_kg,
            patient.region, patient.area, patient.condition, patient.income_lpa,
            patient.smoker, patient.occupation
        )
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_patient_in_db(patient_id: str, updates: dict):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        set_clause = ", ".join([f"{k} = %s" for k in updates])
        values = list(updates.values()) + [patient_id]
        cursor.execute(f"UPDATE patients SET {set_clause} WHERE id = %s", values)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_patient_in_db(patient_id: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# ======================
# Endpoints
# ======================
@app.get("/")
def root():
    return {"message": "Insurance Premium Predictor API"}

@app.get("/about")
def about():
    return {"message": "Predict insurance premium categories and manage patients"}

# Authentication Routes
@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username/email or password")
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return Token(access_token=access_token, token_type="bearer")

@app.post("/auth/register")
def register(email: str, password: str):
    if get_user(email):  # Check if email or generated username exists
        raise HTTPException(400, "Email already registered")
    username = email.split("@")[0].lower()
    if get_user(username):
        raise HTTPException(400, "Username conflict; try a different email")
    hashed_password = get_password_hash(password)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO users (username, email, hashed_password, full_name, disabled)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (username, email, hashed_password, None, False))
        conn.commit()
        cursor.close()
        conn.close()
        return JSONResponse(status_code=201, content={"message": "User registered successfully"})
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

# Users Endpoint (secured)
@app.get("/users")
def get_users(current_user: Annotated[User, Depends(get_current_active_user)]):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username, full_name, email, disabled FROM users")  # Exclude hashed_password
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Patient Endpoints (secured with auth, using MySQL)
@app.get("/view")
def view_patients(current_user: Annotated[User, Depends(get_current_active_user)]):
    data = get_patients()
    # Convert to Patient models for computed fields
    return [Patient(**p).model_dump() for p in data]

# ... (rest of imports and code unchanged)

@app.get('/patient/{id}')
def view_patient(
    id: Annotated[str, Path(description='ID of the patient in the DB', examples=['P001'])],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    # Body unchanged
    patient = get_patient(id)
    if not patient:
        raise HTTPException(status_code=404, detail='Patient not found')
    return Patient(**patient).model_dump()  # Include computed fields
@app.get('/sort')
def sort_patients(
    sort_by: Annotated[str, Query(description='Sort on the basis of height_cm, weight_kg or bmi')],
    current_user: Annotated[User, Depends(get_current_active_user)],  # Move required dependency here (before the default param)
    order: Annotated[str, Query(description='sort in asc or desc order')] = 'asc'  # Default last, outside Query()
):
    valid_fields = ['height_cm', 'weight_kg', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    data = get_patients()
    # For bmi, compute it manually for sorting (since it's computed)
    if sort_by == 'bmi':
        sorted_data = sorted(
            data,
            key=lambda x: (x['weight_kg'] / ((x['height_cm'] / 100) ** 2)) if x['height_cm'] > 0 else 0,
            reverse=(order == 'desc')
        )
    else:
        sorted_data = sorted(
            data,
            key=lambda x: x.get(sort_by, 0),
            reverse=(order == 'desc')
        )
    return [Patient(**p).model_dump() for p in sorted_data]

# ... (other endpoints like /create, /edit, /delete, /predict are fine as-is, since they don't mix =Query/Path with non-defaults)
    valid_fields = ['height_cm', 'weight_kg', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    data = get_patients()
    # For bmi, compute it manually for sorting (since it's computed)
    if sort_by == 'bmi':
        sorted_data = sorted(
            data,
            key=lambda x: (x['weight_kg'] / ((x['height_cm'] / 100) ** 2)) if x['height_cm'] > 0 else 0,
            reverse=(order == 'desc')
        )
    else:
        sorted_data = sorted(
            data,
            key=lambda x: x.get(sort_by, 0),
            reverse=(order == 'desc')
        )
    return [Patient(**p).model_dump() for p in sorted_data]

@app.post('/create')
def create_patient(
    patient: Patient,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    if get_patient(patient.id):
        raise HTTPException(status_code=400, detail='Patient already exists')
    create_patient_in_db(patient)
    return JSONResponse(status_code=201, content={'message': 'patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(
    patient_id: str,
    patient_update: PatientUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    existing = get_patient(patient_id)
    if not existing:
        raise HTTPException(status_code=404, detail='Patient not found')
    updates = patient_update.model_dump(exclude_unset=True)
    if updates:
        update_patient_in_db(patient_id, updates)
    return JSONResponse(status_code=200, content={'message': 'patient updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(
    patient_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    if not get_patient(patient_id):
        raise HTTPException(status_code=404, detail='Patient not found')
    delete_patient_in_db(patient_id)
    return JSONResponse(status_code=200, content={'message': 'patient deleted'})

# Prediction Endpoint (secured)
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
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    # Dummy logic (replace with your real ML model, e.g., load from scikit-learn)
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

















