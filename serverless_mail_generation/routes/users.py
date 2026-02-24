import logging

from fastapi import APIRouter, Depends

from serverless_mail_generation.database import MongoManager, get_database
from serverless_mail_generation.userModel import User
from passlib.context import CryptContext
router = APIRouter()
logger = logging.getLogger(__name__)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.on_event("startup")
async def startup():
    MongoManager.connect()


@router.on_event("shutdown")
async def shutdown():
    MongoManager.close()


def get_users_collection():
    db = get_database()
    return db.get_collection("users")

@router.post("/createUser/{user}")
async def create_user(create_user_request_body: User, collection=Depends(get_users_collection)):
    logger.info("Creating user", create_user_request_body)
    newUser = User(username=create_user_request_body.username, email=create_user_request_body.email,
                   first_name=create_user_request_body.first_name, last_name=create_user_request_body.last_name,
                   role=create_user_request_body.role, hashedPassword=bcrypt_context.hash(create_user_request_body.hashedPassword), isActive=True)
    await collection.insert_one(newUser.model_dump())
    logger.info("Creating user")
