from api.models import RawAggregateData, TeamFormData
from scraper.sites.sofascore import SofaScoreScraper
from scraper.sites.nesine import NesineScraper
from scraper.browser import Browser


async def analyze_match(home: str, away: str) -> RawAggregateData:
    """
    Tüm scraping işlemlerini yöneten ana analiz fonksiyonu.
    """

    browser = Browser()
    await browser.start()

    sofascore = SofaScoreScraper(browser)
    nesine = NesineScraper(browser)

    # Sofascore’dan form bilgisi
    form_home = await sofascore.get_last_5_matches(home)
    form_away = await sofascore.get_last_5_matches(away)

    # Nesine’den oran bilgisi
    odds = await nesine.get_odds(home, away)

    await browser.stop()

    return RawAggregateData(
        home=home,
        away=away,
        form_home=TeamFormData(**form_home),
        form_away=TeamFormData(**form_away),
        odds=odds
    )
