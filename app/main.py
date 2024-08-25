from fastapi import FastAPI, Response, status, HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware

from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import session
from . import models
from .database import engine, sessionLocal,get_db
#from .routers import post,user,auth,vote
from .routers import auth,upload,fieldofficer,farmer,admin
from .config import settings
import os
from dotenv import load_dotenv
from mangum import Mangum

models.Base.metadata.create_all(bind=engine)

app=FastAPI()
handler=Mangum(app)
load_dotenv()


origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(fieldofficer.router)
app.include_router(farmer.router)
app.include_router(admin.router)
@app.get("/")
async def root():
    
        
         print(os.getenv('DATABASE_HOSTNAME'))

         return {"message":
            "welcome to WEFI system that connects farmers with data aggregators and analysts. Welcome All. This system is owned by Bodero"}