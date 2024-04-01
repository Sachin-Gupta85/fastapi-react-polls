"""MongoDB connection helpers.

The app uses a synchronous PyMongo client. `get_db` is a FastAPI dependency so
tests can override it with an in-memory `mongomock` database (no running Mongo
needed to run the test suite).
"""
import os

from pymongo import MongoClient

_client = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(os.environ.get("MONGO_URL", "mongodb://localhost:27017"))
    return _client


def get_db():
    return get_client()[os.environ.get("MONGO_DB", "pollsdb")]
