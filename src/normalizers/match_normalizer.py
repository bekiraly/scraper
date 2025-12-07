from typing import Any, Dict, List

from ..utils.math_utils import safe_div


def normalize_team_fixtures(fixtures: List[Dict[str, Any]], team_id: int) -> List[Dict[str, Any]]:
    """
    API-Football fixtures -> sade format:
    { goals_for, goals_against, is_home, result }
    """
    normalized: List[Dict[str, Any]] = []

    for fix in fixtures:
        teams = fix.get("teams", {})
        goals = fix.get("goals", {})

        home = teams.get("home", {})
        away = teams.get("away", {})

        home_id = home.get("id")
        away_id = away.get("id")

        if home_id == team_id:
            is_home = True
            gf = goals.get("home", 0) or 0
            ga = goals.get("away", 0) or 0
            winner_flag = home.get("winner")
        elif away_id == team_id:
            is_home = False
            gf = goals.get("away", 0) or 0
            ga = goals.get("home", 0) or 0
            winner_flag = away.get("winner")
        else:
            # bu maçta takım yok → atla (normalde olmaz)
            continue

        if winner_flag is True:
            result = "W"
        elif winner_flag is False:
            result = "L"
        else:
            result = "D"

        normalized.append(
            {
                "goals_for": int(gf),
                "goals_against": int(ga),
                "is_home": is_home,
                "result": result,
            }
        )

    return normalized


def summarize_fixtures(fixtures: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Toplam maç sayısı, galibiyet, gol vb. özet."""
    played = len(fixtures)
    wins = sum(1 for f in fixtures if f["result"] == "W")
    draws = sum(1 for f in fixtures if f["result"] == "D")
    losses = sum(1 for f in fixtures if f["result"] == "L")

    goals_for = sum(f["goals_for"] for f in fixtures)
    goals_against = sum(f["goals_against"] for f in fixtures)

    avg_gf = safe_div(goals_for, played)
    avg_ga = safe_div(goals_against, played)

    return {
        "played": played,
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "goals_for": goals_for,
        "goals_against": goals_against,
        "avg_goals_for": avg_gf,
        "avg_goals_against": avg_ga,
    }
