from typing import Any, Dict

from ..data_providers.api_football import APIFootball
from ..features.form_features import compute_form_features
from ..features.goal_features import compute_goal_features
from ..normalizers.match_normalizer import (
    normalize_team_fixtures,
    summarize_fixtures,
)
from ..utils.math_utils import clamp


api = APIFootballClient()


def _compute_strength(form: Dict[str, Any]) -> float:
    """Takım gücünü 0–10 arası kaba bir metrik olarak hesaplar."""
    form_score = float(form["form_score"])  # 0–1
    avg_gf = float(form["avg_goals_for"])
    avg_ga = float(form["avg_goals_against"])

    # Gol yememe bonusu
    defensive_score = clamp(1.0 - avg_ga / 3.0, 0.0, 1.0)

    # 0–10 arası ölçek
    strength = (
        form_score * 5.0  # form
        + avg_gf * 2.0  # hücum
        + defensive_score * 3.0  # defans
    )
    return clamp(strength, 0.0, 10.0)


def _compute_1x2_probabilities(home_strength: float, away_strength: float) -> Dict[str, float]:
    """
    1-0-2 olasılıkları.
    Çok akademik değil ama pratik ve stabil.
    """
    # fark -10..10 civarı → normalize et
    diff = clamp(home_strength - away_strength, -6.0, 6.0)

    # home > away → 1'e ağırlık
    base_home = 0.40 + (diff / 12.0)  # diff=+6 -> +0.5 → 0.9, diff=-6 -> -0.5 → -0.1
    base_away = 0.30 - (diff / 18.0)
    base_draw = 0.30 - abs(diff) / 20.0

    # negatifleri törpüle
    base_home = max(base_home, 0.05)
    base_away = max(base_away, 0.05)
    base_draw = max(base_draw, 0.05)

    total = base_home + base_draw + base_away
    p_home = base_home / total
    p_draw = base_draw / total
    p_away = base_away / total

    return {
        "home_win": round(p_home, 3),
        "draw": round(p_draw, 3),
        "away_win": round(p_away, 3),
    }


def _suggest_scores(
    probs_1x2: Dict[str, float],
    goal_feats: Dict[str, float],
) -> Dict[str, Any]:
    """Olasılıklara göre skor öner."""
    over25 = goal_feats["over25_prob"]
    btts = goal_feats["btts_prob"]

    home_p = probs_1x2["home_win"]
    draw_p = probs_1x2["draw"]
    away_p = probs_1x2["away_win"]

    full_time = []
    first_half = []
    second_half = []

    # Maç gollü mü?
    gollu = over25 > 0.6

    if home_p >= max(draw_p, away_p):
        # Ev favori
        if gollu and btts > 0.6:
            full_time = ["2-1", "3-1"]
        elif gollu:
            full_time = ["2-0", "3-0"]
        else:
            full_time = ["1-0"]
        first_half = ["1-0", "1-1"] if btts > 0.6 else ["1-0"]
        second_half = ["1-1", "2-0"]
        recommended = "1"
    elif away_p >= max(draw_p, home_p):
        # Deplasman favori
        if gollu and btts > 0.6:
            full_time = ["1-2", "1-3"]
        elif gollu:
            full_time = ["0-2", "0-3"]
        else:
            full_time = ["0-1"]
        first_half = ["0-1"]
        second_half = ["0-1", "1-1"]
        recommended = "2"
    else:
        # Beraberlik ağırlıklı
        if gollu and btts > 0.6:
            full_time = ["1-1", "2-2"]
        else:
            full_time = ["0-0", "1-1"]
        first_half = ["0-0", "0-1", "1-0"]
        second_half = ["0-0", "1-1"]
        recommended = "0"

    return {
        "recommended_1x2": recommended,
        "full_time": full_time,
        "first_half": first_half,
        "second_half": second_half,
    }


def predict_match(league: str, season: int, home: str, away: str) -> Dict[str, Any]:
    """
    TEK MOTOR burası:
      - Data Provider
      - Feature Engineering
      - Tahmin Motoru
      - Oran Analizi (şimdilik sadece model)
      - Match Report
    """
    # 1) Takım ID'leri
    home_id = api.get_team_id(home, country=None)
    away_id = api.get_team_id(away, country=None)

    # 2) Son maçlar + H2H
    raw_last_home = api.get_last_fixtures(home_id, last=5)
    raw_last_away = api.get_last_fixtures(away_id, last=5)
    raw_h2h = api.get_head_to_head(home_id, away_id, last=5)

    # 3) Normalize
    norm_home_fixtures = normalize_team_fixtures(raw_last_home, home_id)
    norm_away_fixtures = normalize_team_fixtures(raw_last_away, away_id)

    home_summary = summarize_fixtures(norm_home_fixtures)
    away_summary = summarize_fixtures(norm_away_fixtures)

    # 4) Features
    home_form = compute_form_features(norm_home_fixtures)
    away_form = compute_form_features(norm_away_fixtures)

    goal_feats = compute_goal_features(norm_home_fixtures, norm_away_fixtures)

    home_strength = _compute_strength(home_form)
    away_strength = _compute_strength(away_form)

    probs_1x2 = _compute_1x2_probabilities(home_strength, away_strength)
    score_suggestion = _suggest_scores(probs_1x2, goal_feats)

    # 5) Oran Analizi (şimdilik sadece model bazlı)
    oran_analizi = {
        "not": "Gerçek bahis oranı API'den çekilmiyor (şimdilik). Tahminler sadece modele göre.",
        "guclu_senaryo": score_suggestion["recommended_1x2"],
        "over25_olasilik": round(goal_feats["over25_prob"], 3),
        "btts_olasilik": round(goal_feats["btts_prob"], 3),
    }

    # 6) Match Report (insan dili)
    rec = score_suggestion["recommended_1x2"]
    if rec == "1":
        sonuc_text = "Ev sahibi kazanma ihtimali daha yüksek."
    elif rec == "2":
        sonuc_text = "Deplasman kazanma ihtimali daha yüksek."
    else:
        sonuc_text = "Beraberlik senaryosu öne çıkıyor."

    gollu_text = (
        "Maçın gollü geçme ihtimali yüksek (2.5 üst adayı)."
        if goal_feats["over25_prob"] > 0.6
        else "Gol sayısı orta seviye bekleniyor."
    )
    btts_text = (
        "İki takımın da gol bulma ihtimali yüksek (KG Var adayı)."
        if goal_feats["btts_prob"] > 0.6
        else "KG Var için risk biraz daha yüksek."
    )

    match_report = {
        "kisa": f"{sonuc_text} {gollu_text} {btts_text}",
        "detayli": {
            "home_form": home_form["form_string"],
            "away_form": away_form["form_string"],
            "yorum": sonuc_text,
            "goller": gollu_text,
            "karsilikli_gol": btts_text,
        },
    }

    # 7) Tek JSON çıktısı (senin istediğin başlıklar)
    return {
        "meta": {
            "league": league,
            "season": season,
            "home": home,
            "away": away,
            "home_id": home_id,
            "away_id": away_id,
        },
        "data_provider": {
            "last_home_summary": home_summary,
            "last_away_summary": away_summary,
            "h2h_count": len(raw_h2h),
        },
        "features": {
            "home_form": home_form,
            "away_form": away_form,
            "goal_features": goal_feats,
            "home_strength": home_strength,
            "away_strength": away_strength,
        },
        "tahmin_motoru": {
            "probabilities_1x2": probs_1x2,
            "score_prediction": {
                "full_time": score_suggestion["full_time"],
                "first_half": score_suggestion["first_half"],
                "second_half": score_suggestion["second_half"],
            },
        },
        "oran_analizi": oran_analizi,
        "match_report": match_report,
    }
