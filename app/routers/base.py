from fastapi import APIRouter
from app.routers import auth, register, integrations, recommendation, automations, reminders

api_router = APIRouter()

# Include the routers
api_router.include_router(auth.router)
api_router.include_router(register.router)
api_router.include_router(integrations.router)
api_router.include_router(recommendation.router)
api_router.include_router(automations.router)
api_router.include_router(reminders.router)

