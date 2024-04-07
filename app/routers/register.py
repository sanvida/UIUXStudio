from fastapi import APIRouter, Depends, HTTPException, status

from app.crud.user_manager import UserManager, get_user_manager
from app.schemas.user import UserCreate
from app.models.models import User
 
router = APIRouter()

@router.post(
    "/register",
    response_model=None,
    status_code=status.HTTP_201_CREATED
)
def register(
    user: UserCreate,
    user_manager: UserManager = Depends(get_user_manager),
):

        # Check if user already exists
    db_user = user_manager.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    hashed_password = user_manager.get_hashed_password(user.password)
    user_data = User(username= user.username, email=user.email, full_name=user.full_name, hashed_password=hashed_password)
    created_user = user_manager.create_user(user_data)

    return created_user