from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.models import Recommendation as DBRecommendation, User
from app.schemas.recommendation import Recommendation, RecommendationCreate
from app.routers.security import get_current_user
from app.database import get_db
from typing import List

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/", response_model=List[Recommendation])
def get_recommendations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    recommendations = db.query(DBRecommendation).filter(DBRecommendation.user_id == current_user.id).all()
    return recommendations

@router.post("/", response_model=Recommendation)
def create_recommendation(recommendation: RecommendationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    db_recommendation = DBRecommendation(**recommendation.dict(), user_id=current_user.id)
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    return db_recommendation