import logging
from datetime import date
from pathlib import Path

from playwright.async_api import Playwright, async_playwright

logger = logging.getLogger(__name__)


async def run(
    playwright: Playwright, dest: str | Path, start: date, end: date
) -> None:
    logger.info("Starting playwright")
    chromium = playwright.chromium
    browser = await chromium.launch(headless=True)
    logger.info("Browser launched")
    page = await browser.new_page()
    await page.goto("https://tradingeconomics.com/calendar")

    await page.get_by_role("button", name=" Countries").click()
    await page.get_by_text("Clear").click()

    await page.locator("#te-c-all").get_by_text("United States").click()
    await page.locator("#te-c-all").get_by_text("China").click()
    await page.locator("#te-c-all").get_by_text("Japan").click()
    await page.get_by_text("Save").click()

    await page.wait_for_load_state(timeout=10000)

    await page.get_by_role("button", name=" Dates").click()
    await page.get_by_role("menuitem", name="✏ Custom").click()

    await page.locator("#startDate").fill(start.isoformat())
    await page.locator("#endDate").fill(end.isoformat())
    await page.get_by_role("button", name="Submit").click()

    await page.wait_for_load_state(timeout=10000)

    logger.info("Saving page")
    with open(dest, "w") as f:
        f.write(await page.content())

    logger.info("Closing playwright")
    await browser.close()


async def download(dest: str | Path, start: date, end: date) -> None:
    logger.info(f"Downloading calendar to {dest}")
    async with async_playwright() as playwright:
        await run(playwright, dest, start, end)
