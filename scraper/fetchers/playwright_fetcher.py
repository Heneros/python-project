import random
import time


from loguru import logger
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Error as PlaywrightError,
    Page,
    sync_playwright,
)

from scraper.config import settings
from scraper.fetchers.base import BaseFetcher


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]


BLOCKED_RESOURCES = {"image", "media", "font"}


class PlaywrightFetcher(BaseFetcher):
    def __init__(
        self,
        headless: bool | None = None,
        timeout_ms: int | None = None,
        block_resources: bool = True,
        min_delay: float = 1.0,
        max_delay: float = 3.0,
        max_retries: int = 3,
    ) -> None:
        self.headless = settings.headless if headless is None else headless
        self.timeout_ms = timeout_ms or settings.page_timeout_ms
        self.block_resources = block_resources
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.max_retries = max_retries

        self._playwright = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None

    def __enter__(self) -> "PlaywrightFetcher":
        self._start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def _start(self) -> None:
        logger.info("🚀 Запуск Playwright (headless={})", self.headless)
        self._playwright = sync_playwright().start()

        self._browser = self._playwright.chromium.launch(
            headless=self.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        self._context = self._browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={"width": 1920, "height": 1080},
            locale="en-EN",
            timezone_id="Europe/London",
        )

        self._context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
        )
        if self.block_resources:
            self._context.route("**/*", self._route_handler)

    def close(self) -> None:
        if self._context:
            self._context.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

    logger.info("🛑 Playwright остановлен")

    @staticmethod
    def _route_handler(route) -> None:
        if route.request.resource_type in BLOCKED_RESOURCES:
            route.abort()
        else:
            route.continue_()

    def fetch(self, url: str) -> str | None:
        if self._context is None:
            raise RuntimeError(
                "Fetcher не запущен. Используйте `with PlaywrightFetcher() as f:`"
            )

        for attempt in range(1, self.max_retries + 1):
            page: Page | None = None
            try:
                page = self._context.new_page()
                page.set_default_timeout(self.timeout_ms)
                page.goto(url, wait_until="domcontentloaded")
                html = page.content()
                time.sleep(random.uniform(self.min_delay, self.max_delay))

                return html

            except PlaywrightError as e:
                logger.warning("[{}] Ошибка: {}", attempt, e)
                if attempt == self.max_retries:
                    logger.error("❌ Все попытки исчерпаны для {}", url)
                    return None
                time.sleep(2**attempt)

            finally:
                if page:
                    page.close()

        return None
