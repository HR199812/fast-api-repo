from motor.motor_asyncio import AsyncIOMotorClient
import os

# For local development, this is the default MongoDB URI
MONGODB_URL = "mongodb://localhost:27017"

# Initialize the client
client = AsyncIOMotorClient(MONGODB_URL)

# Reference your specific billing database
# Since you're building a finance dashboard, let's name it 'finance_db'
database = client.test

# This is the 'billing' collection we'll use for the PDFs
billing_collection = database.get_collection("billing")