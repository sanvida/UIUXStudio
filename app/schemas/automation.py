from pydantic import BaseModel

class AutomationBase(BaseModel):
    task_name: str
    details: dict

class AutomationCreate(AutomationBase):
    pass

class Automation(AutomationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
