import requests
from .sofascore import BASE_URL, headers

def get_last_matches(team_id: int, limit: int = 5):
    url = f"{BASE_URL}/team/{team_id}/events/last/0"
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        return []

    data = resp.json()
    events = data.get("events", [])[:limit]

    results = []

    for m in events:
        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]

        score_home = m["homeScore"]["current"]
        score_away = m["awayScore"]["current"]

        # Sonuç (G/B/M)
        if score_home > score_away:
            result = "G"
        elif score_home == score_away:
            result = "B"
        else:
            result = "M"

        results.append({
            "home": home,
            "away": away,
            "score": f"{score_home}-{score_away}",
            "result": result
        })

    return results


def get_form_sequence(team_id: int):
    matches = get_last_matches(team_id)
    if not matches:
        return ""

    return " ".join([m["result"] for m in matches])
