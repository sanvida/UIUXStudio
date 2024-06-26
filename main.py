from fastapi import FastAPI
from app.database import Base, engine
from app.models import models
from app.routers.base import api_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(api_router)