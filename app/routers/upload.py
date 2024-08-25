from typing import Optional, Union,List
from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter,UploadFile
from fastapi.responses import HTMLResponse
from .. import models, schemas, utils,oauth2
from sqlalchemy.orm import session
from ..database import get_db
from sqlalchemy import func
import magic
import boto3
from  uuid import uuid4
from loguru import logger
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from ..config import settings
import logging

router=APIRouter( prefix="/upload",
                  tags=['uploads'])
#configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# aws credentials
#AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
#AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
#AWS_REGION = os.getenv('AWS_REGION')


AWS_ACCESS_KEY_ID = settings.aws_access_key_id
AWS_SECRET_ACCESS_KEY = settings.aws_secret_access_key
AWS_REGION = settings.aws_region

s3 = boto3.resource(
    service_name='s3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


AWS_BUCKET='filetest'
s3=boto3.resource('s3')
bucket=s3.Bucket(AWS_BUCKET)

async def s3_upload(contents: bytes, key: str, subfolder:str='images'):
    full_key = f"{subfolder}/{key}" if subfolder else key
    logger.info(f'Uploading {full_key} to S3')
    try:
        bucket.put_object(Key=full_key, Body=contents, ACL='public-read')
        logger.info(f'Successfully uploaded {full_key} to S3')
    except Exception as e:
        logger.error(f'Failed to upload {full_key} to S3: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to upload file")

KB=1024
MB = 1 * 1024 * 1024

SUPPORTED_FILE_TYPES={
    'image/png':'png',
    'image/jpeg':'jpeg',
    'application/pdf':'pdf'
}

#@router.get("/")
#async def home():
#    return {"welcome":"This is a file upload module to the s3 bucket instance "}

@router.get("/")
async def main():
     content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>File Upload</title>
    </head>
    <body>
        <h1>Upload a file</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    """
     return HTMLResponse(content=content)


@router.post("/")
async def upload(file:UploadFile | None= None,subfolder:str='images'):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="there is no file found in your system"

        )
    contents= await file.read()
    size=len(contents)

    if not 0 < size <= 1*MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="supported file size is 0 to 1MB"
        )
    file_type=magic.from_buffer(buffer=contents, mime=True)

    if file_type not in SUPPORTED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f" unsupported file type: {file_type} the supported ones are:{SUPPORTED_FILE_TYPES}"
        )
    await s3_upload(contents=contents, key=f'{uuid4()}.{SUPPORTED_FILE_TYPES[file_type]}')
    


