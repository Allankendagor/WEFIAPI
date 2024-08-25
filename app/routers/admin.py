from fastapi import APIRouter, Depends, status,HTTPException, Response,FastAPI
from sqlalchemy.orm import session
from typing import Optional
from sqlalchemy.orm import sessionmaker
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database,schemas,models,utils,oauth2
from ..database import get_db
from .. import utils,oauth2

router=APIRouter(prefix="/admin" ,tags=['admin'])


@router.post("/role/registration",status_code=status.HTTP_201_CREATED)
async def admin_reg(user:schemas.UserCreate,db:session=Depends(get_db)):

      # Check if the email already exists
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {user.email} already exists. Please Use another Email"
        )

     
    admin=db.query(models.User).filter(models.User.national_id==user.national_id).first()
    if admin:
          raise HTTPException(
               status_code=status.HTTP_409_CONFLICT,
               detail=f"user with ID of {user.national_id} does  exist. Please Use Your Correct ID"
          )
    

    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=user.model_dump()
    filtered_post_data={
          'email':new_user['email'],
          'First_name':new_user['First_name'],
          'username':new_user['username'],
          'Gender':new_user['Gender'],
          'last_name':new_user['last_name'],
          'national_id':new_user['national_id'],
          'hashed_password':new_user['password']
     }
    created_user=models.User(**filtered_post_data,role="Admin")
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    #generate Access Tokens
    access_token=oauth2.create_access_token(data={"user_id" : created_user.id})
    print(f"Generated token: {access_token}")
    return  {"user": created_user,"access_token": access_token, "token_type": "bearer"}


@router.get("/users")
def users(db:session=Depends(get_db),current_user:int =Depends(oauth2.get_current_admin)):

    users=db.query(models.User).all()
    return users

@router.get("/farmers")
def viewfarmers(db:session=Depends(get_db),current_user:int =Depends(oauth2.get_current_admin)):

    farmers=db.query(models.Farmer).all()

    return farmers

@router.get("/monitor")
def viewfieldmonitoring(db:session=Depends(get_db),current_user:int =Depends(oauth2.get_current_admin)):

    monitor=db.query(models.FieldMonitoring).all()

    return monitor

@router.get("/landprep")
def viewlandprep(db:session=Depends(get_db),current_user:int =Depends(oauth2.get_current_admin)):

    landprep=db.query(models.LandPreparation).all()

    return landprep

@router.get("/farmdetails")
def farmdetails(db:session=Depends(get_db),current_user:int =Depends(oauth2.get_current_admin)):

    farm=db.query(models.FarmDetail).all()

    return farm

@router.get("/yieldata")
def yielddata(db:session=Depends(get_db),current_user:int =Depends(oauth2.get_current_admin)):

    data=db.query(models.YieldData).all()

    return data

@router.get("/profile",response_model=schemas.Profile)
def profile(db:session=Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):

    user_profile=db.query(models.User).filter(models.User.id==current_user.id).first()
    if not user_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile is not found!!")

    return {
        
            "name": user_profile.First_name,
            "avatar": "https://randomuser.me/api/portraits/lego/0.jpg",
            "userid": str(user_profile.id),
            "email": user_profile.email,
            "First_name":user_profile.First_name,
            "last_name":user_profile.last_name,
            "created_at":user_profile.created_at,
            "role":user_profile.role
        
        
    }

@router.post("/logout")
def logout(db:session=Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
     response_data = {
        "data": {},
        "success": True
    }
     if response_data:
          raise HTTPException(
               status_code=status.HTTP_200_OK,
          )
     
     return response_data

