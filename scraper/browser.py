# scraper/browser.py

from playwright.async_api import async_playwright

class Browser:
    def __init__(self):
        self.playwright = None
        self.browser = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)

    async def new_page(self):
        if not self.browser:
            raise RuntimeError("Browser not started")
        return await self.browser.new_page()

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
