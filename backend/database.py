from pymongo import MongoClient
import certifi

MONGO_URI = "YOUR_MONGODB_ATLAS_URI"

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where()
)

db = client["resume_analyzer"]
analysis_collection = db["analysis"]
