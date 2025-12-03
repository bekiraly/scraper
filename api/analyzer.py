from api.models import RawAggregateData, TeamFormData

# SCRAPER IMPORTS (DOĞRU)
from scraper.sites.sofascore import SofaScoreScraper
from scraper.sites.nesine import NesineScraper
from scraper.browser import Browser


async def analyze_match(home: str, away: str):
    """Tüm sitelerden verileri toplayıp unify eder."""

    browser = Browser()

    sofascore = SofaScoreScraper(browser)
    nesine = NesineScraper(browser)

    # Sofascore – Son 5 maç, takım bilgisi
    home_form = await sofascore.get_last_five(home)
    away_form = await sofascore.get_last_five(away)

    # Nesine – Oran, bahis formu vs.
    odds_home, odds_draw, odds_away = await nesine.get_odds(home, away)

    await browser.close()

    return RawAggregateData(
        home=home,
        away=away,
        form_home=home_form,
        form_away=away_form,
        odds_home=odds_home,
        odds_draw=odds_draw,
        odds_away=odds_away,
    )
