class BaseSiteScraper:
    """
    Tüm scraping sınıfları için temel şablon.
    Browser nesnesi Playwright ile dışarıdan verilir.
    """
    def __init__(self, browser):
        self.browser = browser

    async def get_last_5_matches(self, team: str):
        raise NotImplementedError

    async def get_odds(self, home: str, away: str):
        raise NotImplementedError
