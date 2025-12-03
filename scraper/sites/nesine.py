from typing import Optional
from api.models import TeamFormData
from api.scraping.browser import fetch_html
from .base import safe_str
from bs4 import BeautifulSoup  # bunu requirements'a eklemedik, ekleyelim
from scraper.sites.base import BaseSiteScraper

class NesineScraper(BaseSiteScraper):

    async def get_odds(self, home: str, away: str) -> dict:
        """
        Dummy oran bilgisi (gerçek scraping Browser ile yapılacak)
        """
        return {
            "home": 1.80,
            "draw": 3.20,
            "away": 2.40
        }


# requirements.txt'ye ekle: beautifulsoup4

def get_team_form_nesine(team_name: str) -> Optional[TeamFormData]:
    """
    Nesine'den takım formunu kazımaya yönelik iskelet.
    Gerçek HTML selector'ları büyük ihtimalle güncelleme ister.
    """
    # Örn: Nesine istatistik veya takım sayfası URL şablonu:
    # Bu tamamen örnek, sen gerçek URL'yi network tab'dan bakıp düzelteceksin.
    search_url = f"https://www.nesine.com/arama?q={team_name}"
    html = fetch_html(search_url)
    soup = BeautifulSoup(html, "html.parser")

    # Burada takım sayfasına giden ilk linki bulman gerek
    # Örneğin:
    first_team_link = soup.find("a", class_="team-link")
    if not first_team_link or not first_team_link.get("href"):
        return None

    team_url = "https://www.nesine.com" + first_team_link["href"]
    team_html = fetch_html(team_url)
    tsoup = BeautifulSoup(team_html, "html.parser")

    # Son 5 maç tablosunu bul:
    # (Gerçek class/id için sayfayı açıp bakacaksın, burası iskelet)
    form_table = tsoup.find("table", class_="form-table")
    if not form_table:
        return None

    letters = []
    matches = []

    for row in form_table.select("tbody tr")[:5]:
        cols = row.find_all("td")
        if len(cols) < 5:
            continue

        result_text = safe_str(cols[0].get_text())
        home_name = safe_str(cols[1].get_text())
        away_name = safe_str(cols[2].get_text())
        score = safe_str(cols[3].get_text())

        # result_text içinde G/B/M ipucu olabilir
        res = "B"
        if "G" in result_text.upper() or "W" in result_text.upper():
            res = "G"
        elif "M" in result_text.upper() or "L" in result_text.upper():
            res = "M"

        letters.append(res)

        # MatchResult'ı şimdilik sofascore tarafında oluşturduğumuz için
        # Nesine formunu sadece ek bir bilgi olarak kullanacağız.
        # İstersen buraya da MatchResult yapısı ekleyebilirsin.

    if not letters:
        return None

    return TeamFormData(
        team_name=team_name,
        form_string=" ".join(letters),
        matches=[],
    )


def get_match_odds_nesine(home: str, away: str) -> Optional[dict]:
    """
    Maç bülteni sayfasından 1-X-2 oranlarını çekmek için iskelet.
    """
    # Burada ya doğrudan bülten linkine gideceksin
    # ya da site içi aramayla "home - away" maçı bulacaksın.
    # İskelet bırakıyorum:
    return None
