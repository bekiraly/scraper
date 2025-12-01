from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from scraper.sofascore import (
    get_last5,
    get_h2h,
    get_lineup,
    get_coach,
    get_players,
    get_stats,
    get_today_fixtures,
    get_random_fixture_prediction,
)

app = FastAPI(
    title="NewDay AI Analiz API",
    version="0.1.0"
)

# CORS (InfinityFree domainini istersen ekleyebilirsin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Güvenlik için ileride kısıtlarsın
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "service": "NewDay AI Sofascore API"}


# ---------- FORM VE LAST5 ----------

@app.get("/form/{team}")
def form(team: str):
    data = get_last5(team)
    if not data:
        return {"error": "Takım bulunamadı"}
    return data


@app.get("/last5/{team}")
def last5(team: str):
    data = get_last5(team)
    if not data:
        return {"error": "Takım bulunamadı"}
    return data


# ---------- H2H / LINEUP / COACH / PLAYERS / STATS ----------

@app.get("/h2h/{team1}/{team2}")
def h2h(team1: str, team2: str):
    data = get_h2h(team1, team2)
    if not data:
        return {"error": "Takımlar bulunamadı"}
    return data


@app.get("/lineup/{team}")
def lineup(team: str):
    data = get_lineup(team)
    if not data:
        return {"error": "Kadrolar bulunamadı"}
    return data


@app.get("/coach/{team}")
def coach(team: str):
    data = get_coach(team)
    if not data:
        return {"error": "Teknik direktör bilgisi bulunamadı"}
    return data


@app.get("/players/{team}")
def players(team: str):
    data = get_players(team)
    if not data:
        return {"error": "Kadro bilgisi bulunamadı"}
    return data


@app.get("/stats/{team}")
def stats(team: str):
    data = get_stats(team)
    if not data:
        return {"error": "İstatistik bulunamadı"}
    return data


# ---------- FİKSTÜR / TICKER ----------

@app.get("/fixtures/today")
def fixtures_today():
    return {"fixtures": get_today_fixtures()}


@app.get("/fixtures/random")
def fixtures_random():
    data = get_random_fixture_prediction()
    if not data:
        return {"error": "Bugün için fikstür bulunamadı"}
    return data
