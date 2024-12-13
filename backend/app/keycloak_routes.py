import logging
from fastapi import APIRouter, HTTPException, Depends
from app.models.user import UserCreate  # Asegúrate de que este modelo esté disponible
from app.auth.keycloak import verify_token
from pymongo import MongoClient

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Configuración de MongoDB
MONGODB_URI = "mongodb+srv://pedro:1234@cluster0.n22vyn8.mongodb.net/odeonic_test?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI)
db = client['odeonic_test']

@router.post("/keycloak/register")
async def register_user(user: UserCreate):
    logger.info("Intentando registrar un nuevo usuario con email: %s", user.email)
    
    try:
        # Verificar si el usuario ya existe
        existing_user = db.users.find_one({"email": user.email})
        if existing_user:
            logger.warning("El usuario con email %s ya existe.", user.email)
            raise HTTPException(status_code=400, detail="El usuario ya existe")
        
        # Guardar el nuevo usuario en la base de datos
        user_data = {
            "email": user.email,
            "password": user.password,  # Asegúrate de que la contraseña esté hasheada antes de guardar
            "oauth_provider": user.oauth_provider,
            "oauth_id": user.oauth_id
        }
        result = db.users.insert_one(user_data)
        logger.info("Usuario registrado con ID: %s", result.inserted_id)
        
        return {"message": "Usuario registrado exitosamente", "user_id": str(result.inserted_id)}
    except Exception as e:
        logger.error("Error al registrar el usuario: %s", str(e))
        raise HTTPException(status_code=500, detail="Error al registrar el usuario")

@router.get("/keycloak/protected")
async def protected_route(token: str = Depends(verify_token)):
    logger.info("Verificando el token: %s", token)
    # Implementa la lógica de la ruta protegida aquí
