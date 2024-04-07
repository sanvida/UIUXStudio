from pydantic import BaseModel
from datetime import datetime

class ReminderBase(BaseModel):
    message: str
    time: datetime

class ReminderCreate(ReminderBase):
    pass

class Reminder(ReminderBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
