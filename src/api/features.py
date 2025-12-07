from api.models import RawAggregateData
from typing import Dict
import math


def _form_points(form_string: str) -> float:
    """
    G=3, B=1, M=0 puan.
    """
    mapping = {"G": 3, "B": 1, "M": 0}
    total = 0
    for ch in form_string.replace(" ", ""):
        total += mapping.get(ch.upper(), 0)
    return total


def _avg_goal_diff(matches, team_name: str) -> float:
    if not matches:
        return 0.0

    total = 0
    count = 0

    for m in matches:
        if not m.score:
            continue
        try:
            hs, as_ = [int(x.strip()) for x in m.score.split("-")]
        except Exception:
            continue

        home = m.home.lower()
        away = m.away.lower()
        t = team_name.lower()

        diff = 0
        if home == t:
            diff = hs - as_
        elif away == t:
            diff = as_ - hs
        else:
            continue

        total += diff
        count += 1

    if count == 0:
        return 0.0
    return total / count


def _implied_prob(odd: float | None) -> float:
    if not odd or odd <= 1.01:
        return 0.0
    return 1.0 / odd


def build_features(raw: RawAggregateData) -> Dict[str, float]:
    """
    Tüm feature'ları hesaplar.
    """
    home_form_pts = _form_points(raw.home.form_string)
    away_form_pts = _form_points(raw.away.form_string)

    home_goal_trend = _avg_goal_diff(raw.home.matches, raw.home.team_name)
    away_goal_trend = _avg_goal_diff(raw.away.matches, raw.away.team_name)

    # Ruh hali / baskı faktörü (proxy):
    # Lig sıralaması bilgisi yoksa 0 al.
    def _pressure(tf):
        if tf.league_position is None or tf.total_teams is None:
            return 0.0
        # Son 3 ve ilk 3 için baskı
        if tf.league_position <= 3:
            return 0.7
        if tf.league_position >= tf.total_teams - 2:
            return 0.9
        return 0.3

    pressure_home = _pressure(raw.home)
    pressure_away = _pressure(raw.away)

    imp1 = _implied_prob(raw.odds_1)
    impx = _implied_prob(raw.odds_x)
    imp2 = _implied_prob(raw.odds_2)
    s = imp1 + impx + imp2
    if s > 0:
        imp1 /= s
        impx /= s
        imp2 /= s

    features = {
        "form_diff": home_form_pts - away_form_pts,
        "home_goal_trend": home_goal_trend,
        "away_goal_trend": away_goal_trend,
        "goal_trend_diff": home_goal_trend - away_goal_trend,
        "pressure_home": pressure_home,
        "pressure_away": pressure_away,
        "odds_imp1": imp1,
        "odds_impx": impx,
        "odds_imp2": imp2,
    }

    return features
