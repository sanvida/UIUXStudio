from pydantic import BaseModel

class IntegrationBase(BaseModel):
    service_name: str
    details: dict

class IntegrationCreate(IntegrationBase):
    pass

class Integration(IntegrationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
