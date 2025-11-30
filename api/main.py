from fastapi import FastAPI
from scraper.api_football import get_last_five_matches

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "service": "newdayai api running"}

@app.get("/form/{team}")
def form(team: str):
    data = get_last_five_matches(team)

    if not data:
        return {"error": "Takım bulunamadı"}

    return data

from scraper.api_football import HEADERS, API_BASE

@app.get("/fixturetest")
def fixturetest():
    import requests
    url = f"{API_BASE}/fixtures?league=203&season=2024&last=5"
    return requests.get(url, headers=HEADERS).json()
