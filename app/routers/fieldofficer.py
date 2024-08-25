from fastapi import APIRouter, Depends, status,HTTPException, Response,FastAPI
from sqlalchemy.orm import session
from sqlalchemy.orm import sessionmaker
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database,schemas,models,utils,oauth2
from ..database import get_db

router=APIRouter( prefix="/fieldofficer", tags=['fieldofficer'])


@router.post("/role/registration",status_code=status.HTTP_201_CREATED)
def fieldofficer(user:schemas.UserCreate,db:session=Depends(get_db)):
    officer=db.query(models.User).filter(models.User.national_id==user.national_id).first()
    if officer:
          raise HTTPException(
               status_code=status.HTTP_409_CONFLICT,
               detail=f"user with ID of {user.national_id} does  exist in the database. Please Use Your correct ID"
          )
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=user.model_dump()
    filtered_post_data={
          'email':new_user['email'],
          'First_name':new_user['First_name'],
          'last_name':new_user['last_name'],
          'username':new_user['username'],
          'Gender':new_user['Gender'],
          'national_id':new_user['national_id'],
          'hashed_password':new_user['password']
     }
    created_user=models.User(**filtered_post_data,role="Field Officer")
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user
         

@router.post("/", status_code=status.HTTP_201_CREATED)
def registration(post:schemas.FarmerCreate,db:session=Depends(get_db),current_user:int =Depends(oauth2.get_current_field_officer),person:models.User=Depends(oauth2.get_current_user)):
   
    new_reg=models.Farmer(national_id=post.national_id,name=post.name,phone_number=post.phone_number, county=post.county, constituency=post.constituency, ward=post.ward, Gender=post.Gender, nearest_school=post.nearest_school,id_picture=post.id_picture,registered_by=person.First_name)
    db.add(new_reg)
    db.commit()
    db.refresh(new_reg)
    return new_reg


@router.post("/fieldmonitoring")
def fieldmonitoring(post:schemas.FieldMonitoringCreate,db:session=Depends(get_db),current_user:int =Depends(oauth2.get_current_field_officer)):
     farmer=db.query(models.Farmer).filter(models.Farmer.national_id==post.farmer_id).first()
     if farmer is None:
          raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"farmer with ID of {post.farmer_id} does not exist in the database. Please register to use this feature"
          )
     
     new_field=models.FieldMonitoring(
          farmer_id=post.farmer_id,
          date_of_planting=post.date_of_planting, 
          germination_percentage=post.germination_percentage, 
          intercropping=post.intercropping,
          intercrop_details=post.intercrop_details, 
          date_of_weeding=post.date_of_weeding,
          disease_incidence=post.disease_incidence,
          pest_incidence=post.pest_incidence,
          date_of_spraying=post.date_of_spraying,
          expected_date_of_harvest=post.expected_date_of_harvest
          )

     db.add(new_field)
     db.commit()
     db.refresh(new_field)

     return new_field

@router.post("/landprep")
def landpreparation(post:schemas.LandPreparation,db:session=Depends(get_db),current_user:int =Depends(oauth2.get_current_field_officer)):
     farmer=db.query(models.Farmer).filter(models.Farmer.national_id==post.farmer_id).first()
     if farmer is None:
          raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"farmer with ID of {post.farmer_id} does not exist in the database. Please register to use this feature"
          ) 
     new_prep=models.LandPreparation(
          farmer_id=post.farmer_id,
          farm_size=post.farm_size,
          area_ploughed=post.area_ploughed,
          seed_distribution=post.seed_distribution,
          soil_type=post.soil_type,
          gis=post.gis
          )
     
     db.add(new_prep)
     db.commit()
     db.refresh(new_prep)

     return new_prep



@router.post("/yield")
def yielddata(post:schemas.YieldData, db:session=Depends(get_db),current_user:int =Depends(oauth2.get_current_field_officer)):
     farmer=db.query(models.Farmer).filter(models.Farmer.national_id==post.farmer_id).first()
     if farmer is None:
          raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"farmer with ID of {post.farmer_id} does exist in the database. Please register to use this feature"
          )
     new_yield=models.YieldData(
       farmer_id=post.farmer_id,
       yield_data=post.yield_data,
       moisture_content=post.moisture_content
     )
     db.add(new_yield)
     db.commit()
     db.refresh(new_yield)

     return new_yield

@router.post("/farm")
def farmdetail(post:schemas.FarmDetail,  db:session=Depends(get_db),current_user:int =Depends(oauth2.get_current_field_officer)):
     
     farmer=db.query(models.Farmer).filter(models.Farmer.national_id==post.farmer_id).first()
     if farmer is None:
          raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"farmer with ID of {post.farmer_id} does not exist in the database. Please register to use this feature"
          )
     
     farm_data=models.FarmDetail(
          farmer_id=post.farmer_id,
          size=post.size,
          crops=post.crops

     )
     db.add(farm_data)
     db.commit()
     db.refresh(farm_data)

     return farm_data

@router.get("/view/farmers", response_model=list[schemas.Farmer])
def get_farmers(db:session=Depends(get_db), current_user:int=Depends(oauth2.get_current_field_officer),person:models.User=Depends(oauth2.get_current_user)):

     farmers=db.query(models.Farmer).filter(models.Farmer.registered_by==person.First_name).all()

     return farmers
