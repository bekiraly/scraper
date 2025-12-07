from fastapi import APIRouter, Query

from ..engine.prediction_engine import predict_match

router = APIRouter(prefix="/api", tags=["prediction"])


@router.get("/predict")
def predict(
    home: str,
    away: str,
    league: str = Query("TR1", description="Lig kodu (şimdilik sadece meta)"),
    season: int = Query(2024, description="Sezon (şimdilik sadece meta)"),
):
    """
    Örnek:
    /api/predict?home=Galatasaray&away=Samsunspor
    """
    result = predict_match(league=league, season=season, home=home, away=away)
    return result
