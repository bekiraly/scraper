from fastapi import APIRouter
from ..engine.prediction_engine import predict_match

router = APIRouter(prefix="/api")

@router.get("/predict")
def predict(league: str, season: int, home: str, away: str):
    return predict_match(league, season, home, away)
