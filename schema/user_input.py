from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
from config.region_tier import regions, areas


class UserInput(BaseModel):
    # ======================
    # Raw input fields
    # ======================
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
    @field_validator("Region")
    def normalize_region(cls, v: str) -> str:
        return v.strip().title()

    @field_validator("Area")
    def normalize_area(cls, v: str) -> str:
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
        if self.region in regions:
            return 1
        elif self.area in areas:
            return 2
        return 3




        







        