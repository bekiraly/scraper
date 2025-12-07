from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.models import AnalyzeRequest, AnalyzeResponse
from api.analyzer import analyze_match
from api.prediction import predict_from_raw

from scraper.sites.sofascore import SofaScoreScraper
from scraper.sites.nesine import NesineScraper
from scraper.browser import Browser
from fastapi import FastAPI
from .router import router

app = FastAPI(title="NewDayAI - Match Prediction Engine")

app.include_router(router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "service": "NewDay AI Engine"}


@app.post("/analyze")
async def analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    raw = await analyze_match(req.home, req.away)
    pred = predict_from_raw(raw)
    return {
        "home": req.home,
        "away": req.away,
        "form_home": raw.form_home.form_string,
        "form_away": raw.form_away.form_string,
        "prediction": pred.dict()
    }


@app.get("/form/{team}")
async def form(team: str):
    raw = await analyze_match(team, team)
    return {
        "team": team,
        "form": raw.form_home.form_string,
        "matches": [m.dict() for m in raw.form_home.matches]
    }





