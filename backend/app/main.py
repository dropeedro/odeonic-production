from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
import bcrypt
from app.routers import users, plans, secure_data, stripe as stripe_router
from app.auth.keycloak import verify_token
from app.keycloak_routes import router as keycloak_router
from bson.json_util import dumps
import json
import os
from bson import ObjectId
from app.routers.stripe_webhook import router as webhook_router 
from app.routers.keycloak_events import router as keycloak_router
app = FastAPI()

app.include_router(keycloak_router)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Cambia esto según tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 configuración
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Middleware para verificar el token
async def keycloak_auth(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token)
        return payload
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Conexión a MongoDB
MONGODB_URI = "mongodb+srv://pedro:1234@cluster0.n22vyn8.mongodb.net/odeonic_test?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI)


try:
    db = client['odeonic_test']
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error conectando a MongoDB: {e}")

# Modelos Pydantic para validación de entrada y salida

class UserCreate(BaseModel):
    email: EmailStr
    password: str | None = None  # Contraseña opcional para OAuth
    oauth_provider: str | None = None
    oauth_id: str | None = None

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    roles: list[str] = ["user"]  # Asignar rol predeterminado

# Función para hashear la contraseña
def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

# Función para registrar un nuevo usuario
def create_user(user: UserCreate):
    user_data = user.dict()

    # Si el usuario se registra con formulario (sin OAuth), debe tener una contraseña
    if user.password:
        user_data["password"] = hash_password(user.password)
    else:
        # Si es un registro OAuth, no hasheamos la contraseña
        user_data["password"] = None

    # Inserta el nuevo usuario en la colección 'users'
    result = db.users.insert_one(user_data)
    return UserResponse(id=str(result.inserted_id), email=user.email)

# Ruta para registrar usuarios (con o sin OAuth)
@app.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    existing_user = db.users.find_one({"email": user.email})
    
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")
    
    new_user = create_user(user)
    return new_user

@app.get("/")
async def root():
    return {"message": "Welcome to the Odeonic API"}

# Rutas protegidas con autenticación
@app.get("/protected")
async def protected_route(user_data: dict = Depends(keycloak_auth)):
    return {"message": "Welcome to a protected route!", "user": user_data}

# Incluyendo routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(plans.router, prefix="/plans", tags=["Plans"])
app.include_router(secure_data.router, prefix="/secure-data", tags=["Secure Data"])
app.include_router(stripe_router.router, prefix="/stripe", tags=["Stripe"])
app.include_router(keycloak_router, prefix="/keycloak", tags=["Keycloak"])

# Ruta de token
@app.post("/token")
async def login(form_data: OAuth2PasswordBearer = Depends()):
    return {"access_token": "token", "token_type": "bearer"}

# Endpoint para insertar un usuario de prueba
@app.post("/test-insert-user")
def test_insert_user():
    user_data = {
        "email": "testoauthuser@example.com",
        "password": hash_password("password123"),  # Hashea la contraseña
        "oauth_provider": "google",  # Usuario creado vía OAuth
        "oauth_id": "google-oauth-id-123"
    }

    try:
        result = db.users.insert_one(user_data)  # Inserta el usuario en MongoDB
        return {"message": f"Usuario insertado con ID: {result.inserted_id}"}
    except Exception as e:
        return {"error": str(e)}
    # Ruta para obtener todos los usuarios

# Ruta para obtener todos los usuarios de la colección "users"
@app.get("/usuarios", response_model=list[UserResponse])
async def listar_usuarios():
    try:
        usuarios = db.users.find()
        # Formatear la respuesta para devolver solo `id` y `email`
        return [UserResponse(id=str(user["_id"]), email=user["email"]) for user in usuarios]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

from fastapi import Path

# Ruta para bloquear o desbloquear un usuario
@app.put("/usuarios/{user_id}/bloquear")
async def bloquear_usuario(user_id: str):
    # Buscar el usuario en la base de datos
    user = db.users.find_one({"_id": user_id})
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Cambiar el estado de bloqueo (toggle)
    is_blocked = not user.get("isBlocked", False)
    
    # Actualizar el campo 'isBlocked' en la base de datos
    result = db.users.update_one({"_id": user_id}, {"$set": {"isBlocked": is_blocked}})
    
    if result.modified_count == 1:
        return {"isBlocked": is_blocked}
    else:
        raise HTTPException(status_code=500, detail="Error al actualizar el usuario")


app.include_router(plans.router, prefix="/api", tags=["Plans"])

app.include_router(webhook_router, prefix="/api", tags=["Webhook"])

app.include_router(keycloak_router, prefix="/api")

app.include_router(plans.router, prefix="/api/plans", tags=["PlansCRUD"])

