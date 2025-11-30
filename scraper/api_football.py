import os
import requests

API_BASE = "https://v3.football.api-sports.io"

API_KEY = os.getenv("API_FOOTBALL_KEY")
if not API_KEY:
    raise RuntimeError("API_FOOTBALL_KEY environment variable missing")

HEADERS = {
    "x-apisports-key": API_KEY
}

def get_super_lig_season():
    url = f"{API_BASE}/leagues?country=Turkey&name=Super%20Lig"
    res = requests.get(url, headers=HEADERS).json()

    try:
        league_id = res["response"][0]["league"]["id"]
        season = res["response"][0]["seasons"][-1]["year"]
        return league_id, season
    except:
        raise RuntimeError("Super Lig league/season not found")
     
def get_last_five_matches(team):
    league_id, season = get_super_lig_season()

    # find team ID
    url_team = f"{API_BASE}/teams?league={league_id}&season={season}&search={team}"
    res_team = requests.get(url_team, headers=HEADERS).json()

    if not res_team["response"]:
        return {"error": "Takım bulunamadı"}

    team_data = res_team["response"][0]["team"]
    team_id = team_data["id"]
    team_name = team_data["name"]
    logo = team_data["logo"]
    
    # last matches
    url_matches = f"{API_BASE}/fixtures?team={team_id}&season={season}&league={league_id}&last=5"
    res = requests.get(url_matches, headers=HEADERS).json()

    form_letters = []
    matches = []

    for m in res["response"]:
        home = m["teams"]["home"]
        away = m["teams"]["away"]
        score = m["goals"]

        # who won?
        if home["winner"] is True:
            winner = home["name"]
        elif away["winner"] is True:
            winner = away["name"]
        else:
            winner = None

        # form sequence
        if winner is None:
            form_letters.append("B")
        elif winner.lower() == team_name.lower():
            form_letters.append("G")
        else:
            form_letters.append("M")

        matches.append({
            "home": home["name"],
            "away": away["name"],
            "score": f"{score['home']} - {score['away']}"
        })

    return {
        "team_name": team_name,
        "logo": logo,
        "form_string": " ".join(form_letters),
        "matches": matches

    }



