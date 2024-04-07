from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import Reminder as DBReminder, User
from app.schemas.reminder import ReminderCreate, Reminder
from app.routers.security import get_current_user
from app.database import get_db
from typing import List

router = APIRouter(prefix="/reminders", tags=["reminders"])

@router.post("/", response_model=Reminder)
def create_reminder(reminder: ReminderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_reminder = DBReminder(**reminder.dict(), user_id=current_user.id)
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

@router.get("/", response_model=List[Reminder])
def get_reminders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    reminders = db.query(DBReminder).filter(DBReminder.user_id == current_user.id).all()
    return reminders

@router.put("/{reminder_id}", response_model=Reminder)
def update_reminder(reminder_id: int, reminder: ReminderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_reminder = db.query(DBReminder).filter(DBReminder.id == reminder_id, DBReminder.user_id == current_user.id).first()
    if db_reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    db_reminder.message = reminder.message
    db_reminder.time = reminder.time
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

@router.delete("/{reminder_id}", response_model=Reminder)
def delete_reminder(reminder_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_reminder = db.query(DBReminder).filter(DBReminder.id == reminder_id, DBReminder.user_id == current_user.id).first()
    if db_reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    db.delete(db_reminder)
    db.commit()
    return db_reminder
