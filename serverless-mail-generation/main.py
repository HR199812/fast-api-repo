import time

from bson import ObjectId
from fastapi import FastAPI, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer
from database import billing_collection
from ConnectionStatus import ConnectionStatus
from billingModel import InvoiceDocument

app = FastAPI(
    title="My API",
    description="API documentation using Swagger UI",
    version="1.0.0"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/secure")
def secure_route(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@app.get("/invoice/{id}", response_model=InvoiceDocument)
async def get_invoice(id: str = Path(..., description="The hexadecimal ID of the billing record")):
    try:
        record = await billing_collection.find_one({"_id": ObjectId(id)})
        if not record:
            raise HTTPException(status_code=404, detail="Billing record not found")
        return record
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")


@app.get("/test-connection")
async def test_db():
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
