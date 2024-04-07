from fastapi import Depends, HTTPException, Request, status
import jwt
from app.core.config import settings
from app.crud.user_manager import UserManager, get_user_manager


def get_current_user(request: Request, user_manager: UserManager = Depends(get_user_manager)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = request.cookies.get("access_token").replace("Bearer", '').strip()
    if not token:
        raise credentials_exception
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = user_manager.get_user_by_username(username)
        if user is None:
            raise credentials_exception
        return user
    except jwt.PyJWTError:
        raise credentials_exception
