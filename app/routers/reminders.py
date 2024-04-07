from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import Reminder as DBReminder, User
from app.schemas.reminder import ReminderCreate, Reminder
from app.routers.security import get_current_user
from app.database import get_db
from typing import List

router = APIRouter(prefix="/reminders", tags=["reminders"])

@router.post("/", response_model=Reminder, summary="Create Reminder")
def create_reminder(reminder: ReminderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create a new reminder for the current user.

    Parameters:
    - reminder (ReminderCreate): The details of the reminder to be created.

    Returns:
    - Reminder: The created reminder.
    """
    db_reminder = DBReminder(**reminder.dict(), user_id=current_user.id)
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

@router.get("/", response_model=List[Reminder], summary="Get Reminders")
def get_reminders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all reminders for the current user.

    Returns:
    - List[Reminder]: A list of reminders belonging to the current user.
    """
    reminders = db.query(DBReminder).filter(DBReminder.user_id == current_user.id).all()
    return reminders

@router.put("/{reminder_id}", response_model=Reminder, summary="Update Reminder")
def update_reminder(reminder_id: int, reminder: ReminderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Update an existing reminder for the current user.

    Parameters:
    - reminder_id (int): The unique identifier of the reminder to be updated.
    - reminder (ReminderCreate): The updated details of the reminder.

    Returns:
    - Reminder: The updated reminder.
    """
    db_reminder = db.query(DBReminder).filter(DBReminder.id == reminder_id, DBReminder.user_id == current_user.id).first()
    if db_reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    db_reminder.message = reminder.message
    db_reminder.time = reminder.time
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

@router.delete("/{reminder_id}", response_model=Reminder, summary="Delete Reminder")
def delete_reminder(reminder_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Delete an existing reminder for the current user.

    Parameters:
    - reminder_id (int): The unique identifier of the reminder to be deleted.

    Returns:
    - Reminder: The deleted reminder.
    """
    db_reminder = db.query(DBReminder).filter(DBReminder.id == reminder_id, DBReminder.user_id == current_user.id).first()
    if db_reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    db.delete(db_reminder)
    db.commit()
    return db_reminder
