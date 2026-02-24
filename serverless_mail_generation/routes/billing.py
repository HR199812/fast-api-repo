import time
import logging
from fastapi import APIRouter, logger, Depends, HTTPException
from serverless_mail_generation.billingModel import InvoiceDocument
from serverless_mail_generation.ConnectionStatus import ConnectionStatus
from serverless_mail_generation.database import MongoManager

router = APIRouter()
logger = logging.getLogger(__name__)

@router.on_event("startup")
async def startup():
    MongoManager.connect()


@router.on_event("shutdown")
async def shutdown():
    MongoManager.close()


def get_billing_collection():
    db = MongoManager.get_db()
    return db.get_collection("billing")


@router.get("/")
async def root(collection=Depends(get_billing_collection)):
    logger.info("Fetched invoice: %s", await collection.count_documents({}))
    return {"message": "Hello World"}


@router.get("/", tags=["billing"])
async def billing_summary():
    logger.info("Billing summary")


@router.get("/invoice/{id}", response_model=InvoiceDocument)
async def get_invoice(id: str, collection=Depends(get_billing_collection)):
    logger.info("Fetched id: %s", id)
    try:
        record = await collection.find_one({"_id": id})
        logger.info("Fetched invoice: %s", record)
        if not record:
            raise HTTPException(status_code=404, detail="Billing record not found")

        return record

    except Exception as e:
        logger.exception("Error fetching invoice")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/test-connection")
async def test_db(billing_collection=Depends(get_billing_collection)):
    start_time = time.time()
    try:
        # Perform a ping command to verify connectivity
        await billing_collection.database.command("ping")
        end_time = time.time()

        # Calculate latency in milliseconds
        latency = (end_time - start_time) * 1000

        return ConnectionStatus(
            status="success",
            database_name=billing_collection.database.name,
            collection_name=billing_collection.name,
            latency_ms=round(latency, 2),
            message="Successfully connected to local MongoDB instance."
        )
    except Exception as e:
        return ConnectionStatus(
            status="error",
            database_name="unknown",
            collection_name=billing_collection.name,
            message=f"Connection failed: {str(e)}"
        )
