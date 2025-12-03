import requests
from typing import Optional, List
from app.models import TeamFormData, MatchResult
from .base import safe_str

BASE = "https://api.sofascore.com/api/v1"


def _find_team_id(team_name: str) -> Optional[int]:
    url = f"{BASE}/search/all?q={team_name}"
    try:
        r = requests.get(url, timeout=8)
        data = r.json()
    except Exception:
        return None

    top = data.get("topTeams") or data.get("teams") or []
    if not top:
        return None
    return top[0]["id"]


def get_team_form(team_name: str) -> Optional[TeamFormData]:
    team_id = _find_team_id(team_name)
    if not team_id:
        return None

    events_url = f"{BASE}/team/{team_id}/events/last/0"
    try:
        r = requests.get(events_url, timeout=8)
        data = r.json()
    except Exception:
        return None

    events = data.get("events", [])[:5]
    if not events:
        return None

    matches: List[MatchResult] = []
    letters: List[str] = []

    for e in events:
        home_name = safe_str(e["homeTeam"]["name"])
        away_name = safe_str(e["awayTeam"]["name"])
        hs = e["homeScore"].get("current", 0)
        as_ = e["awayScore"].get("current", 0)

        score = f"{hs} - {as_}"
        winner_code = e.get("winnerCode", 0)  # 1=home,2=away,0=draw

        # Kullanıcının takımı ev mi dep mi?
        team_lower = team_name.lower()
        home_lower = home_name.lower()
        away_lower = away_name.lower()

        if winner_code == 0:
            letters.append("B")
        elif winner_code == 1 and home_lower == team_lower:
            letters.append("G")
        elif winner_code == 2 and away_lower == team_lower:
            letters.append("G")
        else:
            letters.append("M")

        matches.append(
            MatchResult(
                home=home_name,
                away=away_name,
                score=score,
                date=str(e.get("startTimestamp", "")),
                home_is_home=(home_lower == team_lower),
            )
        )

    return TeamFormData(
        team_name=team_name,
        form_string=" ".join(letters),
        matches=matches,
        league_position=None,
        total_teams=None,
    )


def get_match_odds(home: str, away: str) -> Optional[dict]:
    """
    Sofascore'dan direkt oran almak zor, placeholder.
    Gerçek oranları Nesine/Bilyoner scraper'ı ile dolduracağız.
    """
    return None
