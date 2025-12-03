from api.models import RawAggregateData
from scraper.sites.sofascore import SofaScoreScraper
from scraper.sites.nesine import NesineScraper
from scraper.browser import Browser


async def analyze_match(home: str, away: str) -> RawAggregateData:
    """
    Tüm sitelerden veri toplayıp tekleştiriyoruz.
    """

    async with Browser() as page:
        ss = SofaScoreScraper(page)
        ns = NesineScraper(page)

        form_home = await ss.get_team_form(home)
        form_away = await ss.get_team_form(away)

        odds = await ns.get_odds(home, away)

        return RawAggregateData(
            home=home,
            away=away,
            form_home=form_home,
            form_away=form_away,
            odds=odds,
        )
