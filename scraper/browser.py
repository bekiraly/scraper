from playwright.async_api import async_playwright

class Browser:
    async def __aenter__(self):
        self.playwright = await async_playwright().start()

        # Railway içinde tarayıcı buraya iniyor
        chrome_path = "/tmp/pw/chromium/chrome-linux/chrome"

        self.browser = await self.playwright.chromium.launch(
            headless=True,
            executable_path=chrome_path,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        self.page = await self.browser.new_page()
        return self.page

    async def __aexit__(self, exc_type, exc, tb):
        await self.browser.close()
        await self.playwright.stop()
