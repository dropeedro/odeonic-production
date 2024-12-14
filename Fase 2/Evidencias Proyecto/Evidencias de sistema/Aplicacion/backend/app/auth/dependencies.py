from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .keycloak import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token)
        return payload  # Devuelve la información del usuario
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
