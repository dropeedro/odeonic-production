from fastapi import APIRouter, HTTPException
from app.models.user import UserCreate, UserResponse
from app.db.user_crud import create_user, get_user_by_email

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def register_user(user: UserCreate):
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    user_id = create_user(user.dict())
    return UserResponse(id=user_id, **user.dict())
