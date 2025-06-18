import os
from motor import motor_asyncio

def get_database():
    try:
        client = motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGO_URI"))
        database = client['seek_db']
        return database
    except Exception as e:
        raise f"Error connecting to database: {e}"
    