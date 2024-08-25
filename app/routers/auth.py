from fastapi import APIRouter, Depends, status,HTTPException, Response,FastAPI
from sqlalchemy.orm import session
from sqlalchemy.orm import sessionmaker
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database,schemas,models,utils,oauth2

router=APIRouter( tags=['Authentication'])



#@router.post("/login",response_model=schemas.Token)
#def login(user_credentials:OAuth2PasswordRequestForm=Depends(), db:session= Depends(database.get_db)):
#      user=db.query(models.User).filter(models.User.username==user_credentials.username).first()
       
#      if not user:
#            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
#      if not utils.verify(user_credentials.password,user.password):
#            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
      
      #create a token
      #return a token
#      access_token=oauth2.create_access_token(data={"user_id":user.id})
#      return {"access_token":access_token ,"token_type":"bearer"}

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db:session = Depends(database.get_db)):
    # Query the user from the database
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    role=db.query(models.User.role).first()
    # If the user is not found, raise an HTTP 403 exception
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # Verify the provided password against the stored hashed password
    if not utils.verify(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
#retrieve the user role from the database
    Role=user.role
    # Create an access token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # Return the access token and its type
    return {"access_token": access_token, "token_type": "bearer","role":Role}