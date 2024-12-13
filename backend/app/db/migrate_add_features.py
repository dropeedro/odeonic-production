from pymongo import MongoClient

# Configura la conexión a MongoDB
DB_USER = 'pedro'
DB_PASSWORD = '1234'
DB_NAME = 'odeonic_test'

client = MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@cluster0.n22vyn8.mongodb.net/{DB_NAME}?retryWrites=true&w=majority")
db = client[DB_NAME]

# Agregar el campo 'features' con un valor predeterminado
result = db.plans.update_many({}, {"$set": {"features": "Default features"}})
print(f"Documentos actualizados: {result.modified_count}")
