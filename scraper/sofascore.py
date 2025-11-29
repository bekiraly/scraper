import requests

BASE_URL = "https://api.sofascore.com/api/v1"
headers = {"User-Agent": "Mozilla/5.0"}

def get_team_id_by_name(team_name: str):
    url = f"{BASE_URL}/search?q={team_name}"
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        return None

    data = resp.json()

    for item in data.get("results", []):
        if item.get("entity") == "team":
            if team_name.lower() in item["name"].lower():
                return item["id"]

    return None
