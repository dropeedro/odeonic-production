from pymongo import MongoClient

MONGODB_URI = "mongodb+srv://pedro:1234@cluster0.n22vyn8.mongodb.net/odeonic_test?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI)

# db = client['odeonic_test']

try:
    client = MongoClient(MONGODB_URI)
    db = client['odeonic_test']
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error conectando a MongoDB: {e}")


