# db/initDB.py
from pymongo import MongoClient
from core.config import settings  # adjust to relative if db is a package

_client = None
_db = None

def init_db_client():
    global _client, _db
    if _db is not None:
        print("MongoDB client already initialized.")
        return _db  # <-- return the db instance here
    _client = MongoClient(settings.MONGO_URI)
    _db = _client[settings.DATABASE_NAME]
    print("MongoDB client initialized.")
    return _db  # <-- return the db instance after init

def get_db():
    global _db
    if _db is None:
        init_db_client()  # This sets _db
    if _db is None:
        raise RuntimeError("MongoDB client not initialized.")
    return _db

