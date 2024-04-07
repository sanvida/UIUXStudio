from sqlalchemy.orm import Session
from fastapi import Depends
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext 
from app.core.config import settings
from app.models import models
from app.database import get_db
from app.schemas.user import UserCreate


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class UserManager:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
    
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_hashed_password(self, password:str):
        return pwd_context.hash(password)

    def get_user_by_username(self, username: str):
        return self.db.query(models.User).filter(models.User.username == username).first()
    
    def authenticate_user(self, username: str, password: str):
        user = self.get_user_by_username(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def create_user(self, user_create: UserCreate): 
        self.db.add(user_create)
        self.db.commit()
        self.db.refresh(user_create)
        return user_create

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

# Dependency
def get_user_manager(db: Session = Depends(get_db)):
    return UserManager(db=db)
