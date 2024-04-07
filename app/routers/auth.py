from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
import datetime

from app.crud.user_manager import UserManager, get_user_manager

router = APIRouter()


@router.post(
    "/login",
    summary="Login to get access token",
    response_description="Logged in successfully",
    tags=["Authentication"]
)
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_manager: UserManager = Depends(get_user_manager)
):
    """
    Endpoint to authenticate users and get an access token for subsequent requests.
    
    Parameters:
    - form_data (OAuth2PasswordRequestForm): The username and password for authentication.
    
    Returns:
    - dict: A message indicating successful login.
    """
    ...
    user = user_manager.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not active",
        )
    
    access_token_expires = datetime.timedelta(minutes=30)
    access_token = user_manager.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # Set secure cookie attributes
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        max_age=access_token_expires.total_seconds(),
        httponly=True,
        secure=True,  # Ensure cookies are sent over HTTPS
        samesite='Lax'  # Mitigate CSRF attacks
    )
    return {"message": "Logged in successfully"}



@router.post(
    "/logout",
    summary="Logout and remove access token cookie",
    response_description="Logged out",
    tags=["Authentication"]
    )
async def logout(response: Response):
    """
    Endpoint to logout and remove the access token cookie.
    
    Returns:
    - dict: A message indicating successful logout.
    """
    response.delete_cookie(
        key="access_token",
        path="/",
    )
    return {"message": "Logged out"}
