from fastapi import FastAPI
from api.models import AnalyzeRequest, AnalyzeResponse
from api.analyzer import analyze_match
from api.prediction import predict_from_raw

from scraper.sites.sofascore import SofaScoreScraper
from scraper.sites.nesine import NesineScraper
from scraper.browser import Browser


app = FastAPI(
    title="NewDay AI Football Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # İleride domain bazlı kısıtlarsın
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "service": "NewDay AI Engine"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    raw = build_raw_aggregate(req.home, req.away)
    pred = predict_from_raw(raw)

    return AnalyzeResponse(
        home=req.home,
        away=req.away,
        form_home=raw.home.form_string,
        form_away=raw.away.form_string,
        prediction=pred,
        raw=raw,
    )




