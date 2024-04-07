from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import Automation as DBAutomation, User
from app.schemas.automation import AutomationCreate, Automation
from app.routers.security import get_current_user
from app.database import get_db
from typing import List

router = APIRouter(prefix="/automations", tags=["automations"])

@router.post("/", response_model=Automation)
def create_automation(automation: AutomationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_automation = DBAutomation(**automation.dict(), user_id=current_user.id)
    db.add(db_automation)
    db.commit()
    db.refresh(db_automation)
    return db_automation

@router.get("/", response_model=List[Automation])
def get_automations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    automations = db.query(DBAutomation).filter(DBAutomation.user_id == current_user.id).all()
    return automations

@router.delete("/{automation_id}", response_model=Automation)
def delete_automation(automation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_automation = db.query(DBAutomation).filter(DBAutomation.id == automation_id, DBAutomation.user_id == current_user.id).first()
    if db_automation is None:
        raise HTTPException(status_code=404, detail="Automation not found")
    db.delete(db_automation)
    db.commit()
    return db_automation
