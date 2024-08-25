from pydantic import BaseModel
from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,Date,Float,LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from pydantic.config import ConfigDict

Base = declarative_base()

class Config:
    arbitrary_types_allowed = True

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username=Column(String,index=True)
    First_name=Column(String)
    last_name=Column(String)
    national_id = Column(Integer, unique=True, index=True)
    hashed_password = Column(String,nullable=False)
    Gender=Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=True)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    

class Farmer(Base):
    __tablename__ = 'farmers'
    id = Column(Integer, primary_key=True, index=True)
    national_id = Column(Integer, unique=True,index=True)
    name = Column(String)
    phone_number = Column(String)
    county = Column(String)
    Gender=Column(String)
    constituency = Column(String)
    ward = Column(String)
    nearest_school = Column(String)
    id_picture = Column(String)
    registered_by=Column(String, nullable=True)
    
    class config:
        arbitrary_types_allowed=True


class FieldMonitoring(Base):
    __tablename__ = 'field_monitoring'
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey('farmers.national_id'))
    date_of_planting = Column(Date)
    germination_percentage = Column(Float)
    intercropping = Column(String)
    intercrop_details = Column(String)
    date_of_weeding = Column(Date)
    disease_incidence = Column(String)
    pest_incidence = Column(String)
    date_of_spraying = Column(Date)
    expected_date_of_harvest = Column(Date)

class LandPreparation(Base):
    __tablename__ = 'land_preparation'
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey('farmers.national_id'))
    farm_size = Column(Float)
    area_ploughed = Column(Float)
    seed_distribution = Column(String)
    soil_type = Column(String)
    gis = Column(String)

class YieldData(Base):
    __tablename__ = 'yield_data'
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey('farmers.national_id'))
    yield_data = Column(Float)
    moisture_content = Column(Float)

class FarmDetail(Base):
    __tablename__ = 'farm_details'
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey('farmers.national_id'))
    size = Column(Float)
    crops = Column(String)