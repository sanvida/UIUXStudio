from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.models import Recommendation as DBRecommendation, User
from app.schemas.recommendation import Recommendation, RecommendationCreate
from app.routers.security import get_current_user
from app.database import get_db
from typing import List

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/", response_model=List[Recommendation], summary="Get Recommendations")
def get_recommendations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all recommendations for the current user.

    Returns:
    - List[Recommendation]: A list of recommendations belonging to the current user.
    """
    recommendations = db.query(DBRecommendation).filter(DBRecommendation.user_id == current_user.id).all()
    return recommendations

@router.post("/", response_model=Recommendation, summary="Create Recommendation")
def create_recommendation(recommendation: RecommendationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Create a new recommendation for the current user.

    Parameters:
    - recommendation (RecommendationCreate): The details of the recommendation to be created.

    Returns:
    - Recommendation: The created recommendation.
    """
    db_recommendation = DBRecommendation(**recommendation.dict(), user_id=current_user.id)
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    return db_recommendation