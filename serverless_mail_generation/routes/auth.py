import logging
from datetime import datetime, timedelta
from typing import Annotated

import timedelta
from fastapi import HTTPException, APIRouter, logger, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from jose import jwt, JWTError
from pydantic import BaseModel

from serverless_mail_generation.database import get_database
from serverless_mail_generation.routes.users import bcrypt_context

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

secret_key = "my-test-jwt-secret-string"
algorithm = "HS256"
logger = logging.getLogger(__name__)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/secure", response_model=Token)
async def secure_route(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                       db: AsyncIOMotorClient = Depends(get_database)):
    user = await db.get_collection("users").find_one({"username": form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not bcrypt_context.verify(form_data.password, user["hashedPassword"]):
        raise HTTPException(status_code=400, detail="Incorrect password")

    token_data = {
        'sub': user["username"],  # Dictionary access with []
        'email': user["email"],
        'id': str(user["_id"]),  # MongoDB uses _id, convert to string
        'exp': datetime.now()  # Token expires in 30 minutes
    }

    return {"access_token": jwt.encode(token_data, secret_key, algorithm), "token_type": "bearer"}


@router.get("/token/{token}")
def decode_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user: str = payload["sub"]
        email: str = payload["email"]
        if user is None or email is None:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        return {user, email}
    except JWTError:
        raise HTTPException(status_code=400, detail="Could not validate credentials")


@router.get("/")
async def authenticate_user(user: str):
    logger.info(f"User authenticated: {user}")
