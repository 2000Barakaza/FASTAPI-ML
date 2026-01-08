from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated, Literal, Optional
from config.region_tier import regions, areas
import json

app = FastAPI()

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

    # ======================
    # Validators
    # ======================
    @field_validator("region")
    def normalize_regions(cls, v: str) -> str:
        return v.strip().title()

    @field_validator("area")
    def normalize_areas(cls, v: str) -> str:
        return v.strip().title()

    # ======================
    # Computed fields
    # ======================
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
        if self.regions in regions:
            return 1
        elif self.areas in areas:
            return 2
        return 3

class PatientUpdate(BaseModel):
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender: Annotated[Optional[str], Field(default=None)]
    height_cm: Annotated[Optional[float], Field(default=None, gt=0, lt=250)]
    weight_kg: Annotated[Optional[float], Field(default=None, gt=0)]
    regions: Annotated[Optional[str], Field(default=None)]
    areas: Annotated[Optional[str], Field(default=None)]
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

def load_data():
    try:
        with open('patients.json', 'r') as f:
            data = json.load(f)
        if isinstance(data, list):
            return {p["id"]: p for p in data}
        return data
    except FileNotFoundError:
        return {}

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {'message':'Patient Management System API'}

@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{id}')
def view_patient(id: str = Path(..., description='ID of the patient in the DB', examples=['P001'])):
    data = load_data()
    if id in data:
        return data[id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height_cm, weight_kg or bmi'), order: str = Query('asc', description='sort in asc or desc order')):
    valid_fields = ['height_cm', 'weight_kg', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    data = load_data()
    sort_order = True if order == 'desc' else False
    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=sort_order
    )
    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201, content={'message':'patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    existing_patient_info = patient_pydantic_obj.model_dump(exclude=['id'])
    data[patient_id] = existing_patient_info
    save_data(data)
    return JSONResponse(status_code=200, content={'message':'patient updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={'message':'patient deleted'})


class PredictionInput(BaseModel):
    age: int
    weight: float
    height: float
    income: float
    smoker: bool
    region: str
    area: str
    occupation: str

@app.post("/predict")
def predict(data: PredictionInput):
    # TEMP: replace with your real ML model
    return {
        "premium_category": "Medium",
        "input_received": data
    }














