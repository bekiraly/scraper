import requests

BASE = "https://api.sofascore.com/api/v1"

def find_team(team):
    url = f"{BASE}/search/all?q={team}"
    r = requests.get(url).json()

    for item in r.get("topTeams", []):
        return item["id"], item["name"]

    for item in r.get("teams", []):
        return item["id"], item["name"]

    return None, None


def get_last5(team):
    team_id, team_name = find_team(team)
    if not team_id:
        return None

    url = f"{BASE}/team/{team_id}/events/last/0"
    r = requests.get(url).json()

    matches = r.get("events", [])[:5]

    form = []
    out = []

    for m in matches:
        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]
        score = f"{m['homeScore']['current']} - {m['awayScore']['current']}"

        winner = m.get("winnerCode", 0)

        if winner == 0:
            form.append("B")
        elif (winner == 1 and home.lower() == team_name.lower()) or \
             (winner == 2 and away.lower() == team_name.lower()):
            form.append("G")
        else:
            form.append("M")

        out.append({
            "home": home,
            "away": away,
            "score": score
        })

    return {
        "team": team_name,
        "form": " ".join(form),
        "matches": out
    }



def get_h2h(team1, team2):
    id1, _ = find_team(team1)
    id2, _ = find_team(team2)
    if not id1 or not id2:
        return None

    url = f"{BASE}/team/{id1}/h2h-standings/{id2}"
    return requests.get(url).json()


def get_lineup(team):
    team_id, _ = find_team(team)
    if not team_id:
        return None

    # last match id
    url = f"{BASE}/team/{team_id}/events/last/0"
    r = requests.get(url).json()
    if not r.get("events"):
        return None

    match_id = r["events"][0]["id"]
    lineup_url = f"{BASE}/event/{match_id}/lineups"
    return requests.get(lineup_url).json()


def get_coach(team):
    team_id, _ = find_team(team)
    url = f"{BASE}/team/{team_id}"
    r = requests.get(url).json()
    return r.get("managers", [])


def get_players(team):
    team_id, _ = find_team(team)
    url = f"{BASE}/team/{team_id}/players"
    return requests.get(url).json()


def get_stats(team):
    team_id, _ = find_team(team)
    url = f"{BASE}/team/{team_id}/statistics"
    return requests.get(url).json()
