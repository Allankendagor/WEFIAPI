from fastapi import APIRouter, Depends, status,HTTPException, Response,FastAPI
from sqlalchemy.orm import session
from sqlalchemy.orm import sessionmaker
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database,schemas,models,utils,oauth2
from ..database import get_db

router=APIRouter(prefix="/farmer" ,tags=['farmer'])


@router.post("/role/registration",status_code=status.HTTP_201_CREATED)
def farmer_reg(user:schemas.UserCreate,db:session=Depends(get_db)):
    farm=db.query(models.User).filter(models.User.national_id==user.national_id).first()
    if farm:
          raise HTTPException(
               status_code=status.HTTP_409_CONFLICT,
               detail=f"user with ID of {user.national_id} does  exist in the database. Please Use your correct National Identification document."
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
    created_user=models.User(**filtered_post_data,role="Farmer")
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user

@router.get("/")
def farmdetails(db:session=Depends(get_db),current_user:int =Depends(oauth2.get_current_farmer)):

    farmers=db.query(models.FarmDetail).all()
    return farmers

@router.get("/yield")
def yielddata(db:session=Depends(get_db),current_user:int =Depends(oauth2.get_current_farmer)):

    farm_yield=db.query(models.YieldData).all()

    return farm_yield