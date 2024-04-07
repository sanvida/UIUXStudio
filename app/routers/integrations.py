from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import Integration as DBIntegration, User
from app.schemas.integration import IntegrationCreate, Integration
from app.routers.security import get_current_user
from app.database import get_db
from typing import List

router = APIRouter(prefix="/integrations", tags=["integrations"])

@router.post("/", response_model=Integration)
def add_integration(integration: IntegrationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_integration = DBIntegration(**integration.dict(), user_id=current_user.id)
    db.add(db_integration)
    db.commit()
    db.refresh(db_integration)
    return db_integration

@router.get("/", response_model=List[Integration])
def get_integrations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    integrations = db.query(DBIntegration).filter(DBIntegration.user_id == current_user.id).all()
    return integrations

@router.delete("/{integration_id}", response_model=Integration)
def delete_integration(integration_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    integration = db.query(DBIntegration).filter(DBIntegration.id == integration_id, DBIntegration.user_id == current_user.id).first()
    if integration is None:
        raise HTTPException(status_code=404, detail="Integration not found")
    db.delete(integration)
    db.commit()
    return integration
