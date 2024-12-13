from pymongo import MongoClient

DB_USER = 'pedro'  # Tu nombre de usuario
DB_PASSWORD = '1234'  # Tu contraseña
DB_NAME = 'odeonic_test'  # Tu nombre de la base de datos

def get_mongo_client():
    client = MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@cluster0.n22vyn8.mongodb.net/{DB_NAME}?ssl=true&ssl_cert_reqs=CERT_NONE")
    return client

db = get_mongo_client()["odeonic_test"]
