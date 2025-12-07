from typing import Any, Dict, List

from ..utils.math_utils import safe_div


def compute_form_features(fixtures: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Son maçlardan:
      - form_string (WWDL…)
      - form_score (0–1 arası)
      - ortalama gol verileri
    """
    played = len(fixtures)
    wins = sum(1 for f in fixtures if f["result"] == "W")
    draws = sum(1 for f in fixtures if f["result"] == "D")
    losses = sum(1 for f in fixtures if f["result"] == "L")

    goals_for = sum(f["goals_for"] for f in fixtures)
    goals_against = sum(f["goals_against"] for f in fixtures)

    avg_gf = safe_div(goals_for, played)
    avg_ga = safe_div(goals_against, played)

    # Form string: yeni maç en sağda gibi
    form_string = "".join(f["result"] for f in fixtures)

    # Basit form score:
    # galibiyet = 3, beraberlik = 1
    points = wins * 3 + draws * 1
    max_points = played * 3 or 1
    points_score = safe_div(points, max_points)

    # Gol dengesi etkisi
    goal_balance = goals_for - goals_against
    goal_score = 0.5 + 0.5 * max(min(goal_balance / 10.0, 1), -1)  # -1..1 -> 0..1

    # Nihai form puanı (0–1)
    form_score = 0.6 * points_score + 0.4 * goal_score

    return {
        "played": played,
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "goals_for": goals_for,
        "goals_against": goals_against,
        "avg_goals_for": avg_gf,
        "avg_goals_against": avg_ga,
        "form_string": form_string,
        "form_score": form_score,
    }
