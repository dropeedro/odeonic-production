from fastapi import APIRouter, HTTPException, Request
from app.database import db  # Importar configuración de MongoDB

router = APIRouter()

@router.post("/keycloak/events")
async def handle_keycloak_event(request: Request):
    """
    Endpoint para manejar eventos de Keycloak.
    """
    try:
        event_data = await request.json()

        # Validar datos esenciales
        event_type = event_data.get("type")
        user_data = event_data.get("user", {})
        if event_type not in ["REGISTER", "LOGIN"]:
            return {"message": f"Evento {event_type} ignorado."}

        user_email = user_data.get("email")
        if not user_email:
            raise HTTPException(status_code=400, detail="Email no proporcionado en el evento.")

        # Verificar si el usuario existe en MongoDB
        existing_user = db.users.find_one({"email": user_email})

        if event_type == "REGISTER" and not existing_user:
            # Crear nuevo usuario si es un registro y no existe
            new_user = {
                "email": user_email,
                "name": f"{user_data.get('firstName', '')} {user_data.get('lastName', '')}".strip(),
                "roles": user_data.get("realmRoles", []),
                "keycloak_id": user_data.get("id"),
                "created_at": event_data.get("time"),
            }
            db.users.insert_one(new_user)
            return {"message": f"Usuario {user_email} registrado exitosamente."}

        if event_type == "LOGIN":
            # Actualizar último acceso si es un login
            db.users.update_one(
                {"email": user_email},
                {"$set": {"last_login": event_data.get("time")}}
            )
            return {"message": f"Usuario {user_email} actualizado exitosamente."}

        return {"message": "Ninguna acción requerida."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar evento: {str(e)}")
