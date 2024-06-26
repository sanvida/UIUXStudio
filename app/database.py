from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator
from app.core.config import settings

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()