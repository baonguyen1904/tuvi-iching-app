import logging

from playwright.async_api import Browser, BrowserContext, async_playwright

logger = logging.getLogger(__name__)

_playwright = None
_browser: Browser | None = None


async def start():
    """Launch Chromium. Call once at FastAPI startup."""
    global _playwright, _browser
    _playwright = await async_playwright().start()
    _browser = await _playwright.chromium.launch(headless=True)
    logger.info("BrowserManager: Chromium launched")


async def new_context() -> BrowserContext:
    """Create isolated browser context for a single scrape request."""
    if _browser is None:
        raise RuntimeError("BrowserManager not started. Call start() first.")
    return await _browser.new_context(
        locale="vi-VN",
        viewport={"width": 694, "height": 1080},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    )


async def shutdown():
    """Close browser and Playwright. Call at FastAPI shutdown."""
    global _browser, _playwright
    if _browser:
        await _browser.close()
        _browser = None
        logger.info("BrowserManager: browser closed")
    if _playwright:
        await _playwright.stop()
        _playwright = None
