import requests
from jose import jwt, JWTError

KEYCLOAK_URL = "http://localhost:8080"  # keycloak url
REALM_NAME = "odeonic-app"  # realm name

def get_public_key():
    url = f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/certs"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["keys"][0] 
    else:
        raise RuntimeError("Could not fetch public key from Keycloak")

def verify_token(token: str):
    try:
        public_key = get_public_key()
        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        return payload
    except JWTError:
        raise ValueError("Invalid token")
    
def has_role(token: str, required_role: str) -> bool:
    payload = verify_token(token)
    roles = payload.get("realm_access", {}).get("roles", [])
    return required_role in roles