import asyncio
import time

from playwright.async_api import Error as PlaywrightError, TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright, Browser, ProxySettings, Page, Playwright
from playwright_stealth import stealth_async
from yarl import URL


def proxy_url_to_playwright_proxy(proxy: str) -> ProxySettings:
    proxy = URL(proxy)
    return ProxySettings(
        server=f"{proxy.scheme}://{proxy.host}:{proxy.port}",
        password=proxy.password,
        username=proxy.user,
    )


class BaseBrowser:
    def __init__(
            self,
            *,
            headless=False,
            default_proxy: str = None,
    ):
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._headless = headless
        self._default_proxy = proxy_url_to_playwright_proxy(default_proxy) if default_proxy else None

    async def create_browser(self):
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=self._headless, proxy=self._default_proxy)

    async def close_browser(self):
        await self._browser.close()
        await self._playwright.stop()

    async def __aenter__(self):
        await self.create_browser()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_browser()
