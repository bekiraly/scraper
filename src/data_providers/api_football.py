import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}


class APIFootball:

    def get_team_id(self, name, country=None):
        """Takım ID bulma"""
        url = f"{BASE_URL}/teams?search={name}"
        res = requests.get(url, headers=HEADERS)
        data = res.json()

        if data.get("results", 0) == 0:
            return None

        # Ülkeye göre filtre (varsa)
        for item in data["response"]:
            if country and item["team"]["country"] != country:
                continue
            return item["team"]["id"]

        # fallback
        return data["response"][0]["team"]["id"]

    def get_last_fixtures(self, team_id, last=5, season=2024):
        """Son maçlar – önce sezonlu, sonra fallback"""

        # 1) Sezonlu dene
        url = f"{BASE_URL}/fixtures?team={team_id}&season={season}&last={last}"
        res = requests.get(url, headers=HEADERS)
        data = res.json()

        # 2) Sonuç yoksa sezonsuz fallback
        if data.get("results", 0) == 0:
            url = f"{BASE_URL}/fixtures?team={team_id}&last={last}"
            res = requests.get(url, headers=HEADERS)
            data = res.json()

        # 3) Hâlâ yoksa boş liste
        if data.get("results", 0) == 0:
            return []

        return data["response"]

    def get_head_to_head(self, team1, team2, last=5):
        """H2H Son Maçlar"""
        url = f"{BASE_URL}/fixtures/headtohead?h2h={team1}-{team2}&last={last}"
        res = requests.get(url, headers=HEADERS)
        data = res.json()

        if data.get("results", 0) == 0:
            return []

        return data["response"]
