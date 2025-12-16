import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv('.env.local')

MONGODB_URI = os.environ.get("MONGODB_URI")

if not MONGODB_URI:
    try:
        load_dotenv('.env')
        MONGODB_URI = os.environ.get("MONGODB_URI")
    except:
        pass

if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable not set")

client = MongoClient(MONGODB_URI)
db = client.get_default_database()

def get_database():
    return db

def get_collection(collection_name):
    return db[collection_name]

def close_connection():
    client.close()

# Test connection
try:
    client.admin.command('ping')
    print("MongoDB connection successful!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
