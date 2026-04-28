import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

print("MONGO_URI loaded:", MONGO_URI)
print("MONGO_DB_NAME loaded:", MONGO_DB_NAME)

if not MONGO_URI or not MONGO_DB_NAME:
    raise ValueError("MONGO_URI or MONGO_DB_NAME is missing from .env file")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]
task_collection = db["tasks"]