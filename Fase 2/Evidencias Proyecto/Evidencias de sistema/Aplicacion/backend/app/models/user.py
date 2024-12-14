from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str | None = None
    oauth_provider: str | None = None
    oauth_id: str | None = None

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    roles: list[str] = ["user"]  # Asignar rol predeterminado
