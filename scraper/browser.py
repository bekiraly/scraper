from playwright.async_api import async_playwright

class Browser:
    async def __aenter__(self):
        self.play = await async_playwright().start()
        self.browser = await self.play.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        self.page = await self.browser.new_page()
        return self.page

    async def __aexit__(self, exc_type, exc, tb):
        await self.browser.close()
        await self.play.stop()
