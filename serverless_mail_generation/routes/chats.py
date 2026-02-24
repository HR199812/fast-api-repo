import logging

from fastapi import APIRouter
from fastapi.params import Depends
from serverless_mail_generation.chatsModel import Chat
from serverless_mail_generation.database import MongoManager

router = APIRouter()
logger = logging.getLogger(__name__)


@router.on_event("startup")
async def startup():
    MongoManager.connect()


@router.on_event("shutdown")
async def shutdown():
    MongoManager.close()


def get_chat_collection():
    db = MongoManager.get_db()
    return db.get_collection("chats")


@router.get("/chats/", tags=["chats"])
async def root(chat_collection=Depends(get_chat_collection), response_model=Chat):
    logger.info("I am called")
    chats = await chat_collection.find({}, {
        "createdAt": 0,
        "updatedAt": 0,
        "__v": 0,
        "_id": 0
    }).to_list(length=None)

    logger.info(f"Chats: {chats}")
    return chats
