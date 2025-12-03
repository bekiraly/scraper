from scraper.sites.base import BaseSiteScraper


class SofaScoreScraper(BaseSiteScraper):

    async def get_last_5_matches(self, team: str):
        return {
            "team": team,
            "form": ["G", "G", "M", "B", "G"],
            "scores": ["3-1", "2-0", "1-2", "1-1", "4-1"]
        }

    async def get_odds(self, home: str, away: str):
        return {
            "home": 1.95,
            "draw": 3.20,
            "away": 2.30
        }
