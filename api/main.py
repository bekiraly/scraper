from fastapi import FastAPI
from scraper.sofascore import get_team_id_by_name
from scraper.matches import get_form_sequence

app = FastAPI()

@app.get("/form/{team_name}")
def form(team_name: str):
    team_id = get_team_id_by_name(team_name)

    if not team_id:
        return {"error": "Takım bulunamadı"}

    form_data = get_form_sequence(team_id)

    return {
        "team": team_name,
        "form": form_data
    }
