from typing import Any, Dict, List

from ..utils.math_utils import clamp, safe_div


def compute_goal_features(
    home_fixtures: List[Dict[str, Any]],
    away_fixtures: List[Dict[str, Any]],
) -> Dict[str, float]:
    """Genel gol eğilimlerini çıkartır."""
    home_played = len(home_fixtures) or 1
    away_played = len(away_fixtures) or 1

    # Maç başı gol verileri
    home_goals_for = sum(f["goals_for"] for f in home_fixtures)
    home_goals_against = sum(f["goals_against"] for f in home_fixtures)
    away_goals_for = sum(f["goals_for"] for f in away_fixtures)
    away_goals_against = sum(f["goals_against"] for f in away_fixtures)

    home_avg_for = safe_div(home_goals_for, home_played)
    home_avg_against = safe_div(home_goals_against, home_played)
    away_avg_for = safe_div(away_goals_for, away_played)
    away_avg_against = safe_div(away_goals_against, away_played)

    # Gol attığı maç oranı
    home_scored_rate = safe_div(
        sum(1 for f in home_fixtures if f["goals_for"] > 0), home_played
    )
    away_scored_rate = safe_div(
        sum(1 for f in away_fixtures if f["goals_for"] > 0), away_played
    )

    # Gol yediği maç oranı
    home_concede_rate = safe_div(
        sum(1 for f in home_fixtures if f["goals_against"] > 0), home_played
    )
    away_concede_rate = safe_div(
        sum(1 for f in away_fixtures if f["goals_against"] > 0), away_played
    )

    # KG Var tahmini (iki taraf da atar mı?)
    btts_prob = clamp(
        (home_scored_rate + away_scored_rate + home_concede_rate + away_concede_rate)
        / 4.0,
        0.1,
        0.95,
    )

    # Maç toplam gol potansiyeli
    avg_total_goals = (home_avg_for + away_avg_for + home_avg_against + away_avg_against) / 4.0
    # 0–4 arası normalize et
    goal_potential = clamp(avg_total_goals / 3.0, 0.1, 1.0)

    # 2.5 üst olasılığı (basit mapping)
    over25_prob = clamp(0.3 + goal_potential * 0.5, 0.1, 0.95)

    # İlk yarı / ikinci yarı daha kaba tahminler
    # Toplam gol potansiyelini oranlayalım:
    first_half_goal_prob = clamp(0.4 + goal_potential * 0.3, 0.1, 0.9)
    second_half_goal_prob = clamp(0.5 + goal_potential * 0.3, 0.1, 0.95)

    return {
        "home_avg_for": home_avg_for,
        "home_avg_against": home_avg_against,
        "away_avg_for": away_avg_for,
        "away_avg_against": away_avg_against,
        "avg_total_goals": avg_total_goals,
        "goal_potential": goal_potential,
        "btts_prob": btts_prob,
        "over25_prob": over25_prob,
        "first_half_goal_prob": first_half_goal_prob,
        "second_half_goal_prob": second_half_goal_prob,
    }
