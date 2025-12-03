from typing import Dict
import math
from api.models import PredictionOutput, RawAggregateData
from api.features import build_features


def _score_home(f: Dict[str, float]) -> float:
    return (
        0.6 * f["form_diff"] +
        0.8 * f["goal_trend_diff"] +
        0.5 * (f["pressure_home"] - f["pressure_away"]) +
        1.2 * (f["odds_imp1"] - f["odds_imp2"]) +
        0.3 * (f["odds_imp1"] - f["odds_impx"])
    )


def _score_away(f: Dict[str, float]) -> float:
    return (
        -0.6 * f["form_diff"] -
        0.8 * f["goal_trend_diff"] +
        0.5 * (f["pressure_away"] - f["pressure_home"]) +
        1.2 * (f["odds_imp2"] - f["odds_imp1"]) +
        0.3 * (f["odds_imp2"] - f["odds_impx"])
    )


def _score_draw(f: Dict[str, float]) -> float:
    # Form farkı küçük, goal trend farkı düşük ve impx güçlü ise beraberlik
    return (
        -0.4 * abs(f["form_diff"]) -
        0.6 * abs(f["goal_trend_diff"]) +
        1.0 * f["odds_impx"]
    )


def _softmax3(a: float, b: float, c: float):
    exps = [math.exp(a), math.exp(b), math.exp(c)]
    s = sum(exps)
    return [e / s for e in exps]


def predict_from_raw(raw: RawAggregateData) -> PredictionOutput:
    f = build_features(raw)

    s_home = _score_home(f)
    s_away = _score_away(f)
    s_draw = _score_draw(f)

    ph, pd, pa = _softmax3(s_home, s_draw, s_away)

    reasoning_parts = []

    if f["form_diff"] > 0:
        reasoning_parts.append("Ev sahibi son maçlarda daha formda.")
    elif f["form_diff"] < 0:
        reasoning_parts.append("Deplasman ekibi form avantajına sahip.")

    if f["goal_trend_diff"] > 0:
        reasoning_parts.append("Ev sahibinin gol farkı trendi olumlu.")
    elif f["goal_trend_diff"] < 0:
        reasoning_parts.append("Deplasmanın gol farkı trendi daha iyi.")

    if f["odds_imp1"] > max(f["odds_imp2"], f["odds_impx"]):
        reasoning_parts.append("Piyasa oranları ev sahibini favori gösteriyor.")
    elif f["odds_imp2"] > max(f["odds_imp1"], f["odds_impx"]):
        reasoning_parts.append("Piyasa oranları deplasmanı favori gösteriyor.")
    else:
        reasoning_parts.append("Piyasa oranları dengeli, beraberlik ihtimali öne çıkıyor.")

    reasoning = " ".join(reasoning_parts) or "İstatistiksel dengeye göre hesaplandı."

    return PredictionOutput(
        home_prob=float(ph),
        draw_prob=float(pd),
        away_prob=float(pa),
        reasoning=reasoning,
    )
