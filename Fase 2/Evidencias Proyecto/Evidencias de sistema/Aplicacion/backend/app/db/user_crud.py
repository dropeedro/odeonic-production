from pymongo import MongoClient
from passlib.context import CryptContext

client = MongoClient("mongodb://localhost:27017/")
db = client.odeonic
users_collection = db.users

# Configuración de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(email: str):
    return users_collection.find_one({"email": email})

def create_user(user_data: dict):
    result = users_collection.insert_one(user_data)
    return str(result.inserted_id)
