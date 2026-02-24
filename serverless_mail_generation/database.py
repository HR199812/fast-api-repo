# database.py

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os


class MongoManager:
    _client: AsyncIOMotorClient | None = None

    @classmethod
    def connect(cls):
        if cls._client is None:
            cls._client = AsyncIOMotorClient(
                os.getenv("MONGODB_URL", "mongodb://localhost:27017"),
                maxPoolSize=10,
                minPoolSize=1,
            )

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        if cls._client is None:
            raise RuntimeError("MongoDB client not initialized. Call connect() first.")
        return cls._client["test"]

    @classmethod
    def close(cls):
        if cls._client:
            cls._client.close()
            cls._client = None


def get_database() -> AsyncIOMotorDatabase:
    return MongoManager.get_db()
