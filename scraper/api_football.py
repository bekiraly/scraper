import os
import requests

API_BASE = "https://v3.football.api-sports.io"

def get_last_five_matches(team):
    API_KEY = os.getenv("API_FOOTBALL_KEY")
    if not API_KEY:
        raise RuntimeError("API_FOOTBALL_KEY env değişkeni yok.")

    headers = {"x-apisports-key": API_KEY}
    }


def get_super_lig_league_and_season():
    """
    Türkiye Süper Lig için aktif sezon + lig ID'sini bul.
    """
    url = f"{API_BASE}/leagues"
    params = {
        "country": "Turkey",
        "name": "Super Lig"
    }
    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if not data.get("response"):
        raise ValueError("Super Lig bulunamadı")

    # En güncel sezonu al
    league_info = data["response"][0]
    league_id = league_info["league"]["id"]
    seasons = league_info["seasons"]

    # isCurrent = true olanı bul
    current = next((s for s in seasons if s.get("current")), None)
    if not current:
        # yoksa en son sezonu al
        current = seasons[-1]

    season_year = current["year"]
    return league_id, season_year


def get_team_id(team_name: str):
    """
    İsimden takımı bul, Süper Lig + aktif sezon filtresiyle.
    """
    league_id, season_year = get_super_lig_league_and_season()

    url = f"{API_BASE}/teams"
    params = {
        "search": team_name,
        "league": league_id,
        "season": season_year,
    }
    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if not data.get("response"):
        return None, None, None

    team_info = data["response"][0]
    tid = team_info["team"]["id"]
    name = team_info["team"]["name"]
    logo = team_info["team"]["logo"]

    return tid, name, logo


def get_last_five_matches(team_name: str):
    """
    Son 5 maçı ve form datasını döndür (G/B/M + istatistikler).
    """
    team_id, official_name, logo = get_team_id(team_name)
    if not team_id:
        return None

    league_id, season_year = get_super_lig_league_and_season()

    url = f"{API_BASE}/fixtures"
    params = {
        "team": team_id,
        "league": league_id,
        "season": season_year,
        "last": 5
    }
    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    fixtures = data.get("response", [])

    results = []
    form_letters = []

    for f in fixtures:
        home = f["teams"]["home"]["name"]
        away = f["teams"]["away"]["name"]
        goals_home = f["goals"]["home"]
        goals_away = f["goals"]["away"]

        # Sonuç harfi
        if f["teams"]["home"]["id"] == team_id:
            # bizim takım ev sahibi
            if goals_home > goals_away:
                res = "G"
            elif goals_home == goals_away:
                res = "B"
            else:
                res = "M"
        else:
            # bizim takım deplasman
            if goals_away > goals_home:
                res = "G"
            elif goals_away == goals_home:
                res = "B"
            else:
                res = "M"

        form_letters.append(res)

        # Basit istatistikler (varsa)
        stats = f.get("statistics", [])
        # Şimdilik boş bırakıyoruz, sonra doldururuz

        results.append({
            "home": home,
            "away": away,
            "score": f"{goals_home}-{goals_away}",
            "result": res,
        })

    return {
        "team_id": team_id,
        "team_name": official_name,
        "logo": logo,
        "form_string": " ".join(form_letters[::-1]),  # eskiden yeniye ters çevir
        "matches": list(reversed(results))           # kronolojik olsun diye ters çevir
    }

