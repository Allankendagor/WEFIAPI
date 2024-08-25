from pydantic import BaseModel,EmailStr
from typing import Optional, List
from datetime import date,datetime
from sqlalchemy import LargeBinary

class UserCreate(BaseModel):
    email: EmailStr
    national_id: int
    First_name:str
    last_name:str
    username:str
    Gender:str
    password: str

class Token(BaseModel):
      access_token:str
      token_type:str
      role:str

class TokenData(BaseModel):
      id:int
      role:str

class Profile(BaseModel):
    First_name:str
    last_name:str
    role:str
    created_at:datetime
    name:str
    avatar:str
    userid:int
    email:str
      
class UserOut(BaseModel):
     id:int
     email:str
     national_id:int
     role:str
     first_name:str
     last_name:str 
     created_at: datetime
     registered_by: str

     class Config:
        orm_mode=True

class FarmerCreate(BaseModel):
    national_id: str
    name: str
    phone_number: str
    county: str
    constituency: str
    ward: str
    Gender:str
    nearest_school: str
    id_picture: str

class Farmer(BaseModel):
    id: int
    national_id: int
    name: str
    phone_number: str
    county: str
    constituency: str
    ward: str
    Gender:str
    nearest_school: str
    id_picture: str

    class Config:
        orm_mode = True

class FieldMonitoringCreate(BaseModel):
    farmer_id: int
    date_of_planting: date
    germination_percentage: float
    intercropping: str
    intercrop_details: str
    date_of_weeding: date
    disease_incidence: str
    pest_incidence: str
    date_of_spraying: date
    expected_date_of_harvest: date

class FieldMonitoring(BaseModel):
    id: int
    farmer_id: int
    date_of_planting: date
    germination_percentage: float
    intercropping: str
    intercrop_details: str
    date_of_weeding: date
    disease_incidence: str
    pest_incidence: str
    date_of_spraying: date
    expected_date_of_harvest: date

    class Config:
        orm_mode = True

class LandPreparation(BaseModel):
    farmer_id: int
    farm_size:float
    area_ploughed:float
    seed_distribution:str
    soil_type:str
    gis:str

    class Config:
        orm_mode = True

class YieldData(BaseModel):
    farmer_id:int
    yield_data:float
    moisture_content:float

    class Config:
        orm_mode = True

class FarmDetail(BaseModel):
    farmer_id:int
    size:float
    crops:str





