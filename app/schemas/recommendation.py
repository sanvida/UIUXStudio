from pydantic import BaseModel

class RecommendationBase(BaseModel):
    content: str

class RecommendationCreate(RecommendationBase):
    pass

class Recommendation(RecommendationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
