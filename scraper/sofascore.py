import requests

BASE_URL = "https://api.sofascore.com/api/v1"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_team_id_by_name(team_name: str):
    """
    Sofascore'da takım adını arayıp ID döndürür.
    Örn: get_team_id_by_name("konyaspor") → 6034 gibi.
    """
    url = f"{BASE_URL}/search?q={team_name}"
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        return None

    data = resp.json()

    results = data.get("results", [])
    for item in results:
        if item.get("entity") == "team":
            if team_name.lower() in item["name"].lower():
                return item["id"]

    return None
