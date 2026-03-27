"""Run manually to capture HTML fixtures from live sites.

Usage:
    cd backend && python -m tests.capture_fixtures
"""
import asyncio
import json
from datetime import datetime
from pathlib import Path

from app.services import scraper_browser
from app.services.scraper_browser import new_context
from app.services import constants

FIXTURES_DIR = Path(__file__).parent / "fixtures"


async def capture_cohoc():
    context = await new_context()
    page = await context.new_page()

    dob = datetime(1997, 10, 11)
    time_val = 12  # 21h-23h

    await page.goto(constants.COHOC_FORM_URL)
    await page.wait_for_selector("#btGiaiDoan", timeout=15000)

    await page.locator(f"//select[@name='ddlNgay']/option[text()='{dob.day}']").click()
    await page.locator(f"//select[@name='ddlThang']/option[text()='{dob.month}']").click()
    await page.locator(f"//select[@name='ddlNam']/option[text()='{dob.year}']").click()
    await page.locator(f"//select[@name='ddlGio']/option[@value='{time_val}']").click()
    await page.locator("//input[@name='GioiTinh'][@value='rdNam']").click()
    await page.evaluate('document.getElementById("btGiaiDoan").click()')

    await page.wait_for_selector("div.thien-ban", timeout=90000)
    html = await page.content()
    (FIXTURES_DIR / "cohoc_result.html").write_text(html, encoding="utf-8")
    print(f"Saved cohoc_result.html ({len(html)} bytes)")

    from app.services.scraper_cohoc import parse_body
    data = parse_body(html)
    (FIXTURES_DIR / "cohoc_expected.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("Saved cohoc_expected.json")

    await context.close()


async def capture_tuvivn():
    context = await new_context()
    page = await context.new_page()

    dob = datetime(1997, 10, 11, 12, 0)

    await page.goto(constants.TUVIVN_FORM_URL)
    await page.wait_for_timeout(3000)

    await page.locator('input[name="name"]').fill("Test User")
    await page.locator(f"//select[@name='dayOfDOB']/option[text()='{dob.day}']").click()
    await page.locator(f"//select[@name='monthOfDOB']/option[text()='Tháng {dob.month}']").click()
    year_input = page.locator('input[name="yearOfDOB"]')
    await year_input.clear()
    await year_input.fill(str(dob.year))
    await page.locator(f"//select[@name='hourOfDOB']/option[text()='{dob.hour} Giờ']").click()
    await page.locator(f"//select[@name='minOfDOB']/option[text()='{dob.minute} Phút']").click()
    calendar_radios = page.locator('input[name="calendar"]')
    if await calendar_radios.count() > 0:
        await calendar_radios.first.click()
    gender_radios = page.locator('input[name="gender"]')
    await gender_radios.first.click()

    await page.locator("//button[@type='submit' and contains(text(), 'Lập lá số')]").click()
    try:
        await page.wait_for_selector("td.cung", timeout=15000)
    except Exception:
        pass
    await page.wait_for_timeout(2000)

    html = await page.content()
    (FIXTURES_DIR / "tuvivn_result.html").write_text(html, encoding="utf-8")
    print(f"Saved tuvivn_result.html ({len(html)} bytes)")

    from app.services.scraper_tuvivn import parse_body
    data = parse_body(html)
    serializable = {
        "am_duong": data["am_duong"],
        "nam": data["nam"],
        "menh": data["menh"],
        "cung_count": len(data["cung"]),
    }
    (FIXTURES_DIR / "tuvivn_expected.json").write_text(
        json.dumps(serializable, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("Saved tuvivn_expected.json")

    await context.close()


async def main():
    await scraper_browser.start()
    try:
        print("=== Capturing cohoc.net fixture ===")
        await capture_cohoc()
        print("\n=== Capturing tuvi.vn fixture ===")
        await capture_tuvivn()
    finally:
        await scraper_browser.shutdown()

    print("\nDone! Fixtures saved to backend/tests/fixtures/")


if __name__ == "__main__":
    asyncio.run(main())
