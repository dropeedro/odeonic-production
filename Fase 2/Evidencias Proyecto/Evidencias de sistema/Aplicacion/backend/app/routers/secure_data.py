from fastapi import APIRouter, Depends
from ..auth.dependencies import get_current_user

router = APIRouter()

@router.get("/secure-data")
def read_secure_data(user: dict = Depends(get_current_user)):
    return {"message": "This is secure data", "user": user}
