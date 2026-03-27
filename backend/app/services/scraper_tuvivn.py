import logging
import unicodedata
from datetime import datetime
from typing import Optional

from bs4 import BeautifulSoup

from app.models import schemas
from app.services import constants, soup_utils
from app.services.scraper_browser import new_context

logger = logging.getLogger(__name__)

URL = constants.TUVIVN_FORM_URL


def to_string(text: str):
    text = unicodedata.normalize("NFC", text)
    text = text.replace("-", "").replace("+", "")
    parts = text.split()
    parts = [p.strip() for p in parts if p.strip()]
    return " ".join(parts)


def parse_body(body):
    soup = BeautifulSoup(body, "html.parser")

    container = "div.view-thien-ban"
    data = {
        "nam": soup_utils.find_metadata_field(soup, "Năm:", container),
        "menh": to_string(soup_utils.find_metadata_field(soup, "Bản mệnh:", container) or ""),
        "cuc": "",
        "menh_chu": soup_utils.find_metadata_field(soup, "Chủ mệnh:", container),
        "than_chu": soup_utils.find_metadata_field(soup, "Chủ thân:", container),
        "am_duong": soup_utils.find_metadata_field(soup, "Âm dương:", container),
        "cung": [],
    }

    # 12 Cung
    main_order = constants.MAIN_ORDER
    reversed_order = constants.REVERSED_ORDER
    cung_tds = soup.select("td.cung")

    cungs = []
    for td in cung_tds:
        el = td.select_one("p.text-sao-chinh-tinh")
        name = to_string(el.text) if el else ""
        cungs.append(name)

    start = unicodedata.normalize("NFC", "Mệnh")
    start_idx = None
    for idx, name in enumerate(cungs):
        if unicodedata.normalize("NFC", name) == start:
            start_idx = idx
            break

    if start_idx is None:
        raise ValueError(f"Could not find '{start}' cung. Found: {cungs}")

    am_duong = data.get("am_duong", "")
    if am_duong in ["Dương Nam", "Âm Nữ"]:
        idx_in_main = main_order.index(start_idx)
        order = main_order[idx_in_main:] + main_order[:idx_in_main]
    else:
        idx_in_main = reversed_order.index(start_idx)
        order = reversed_order[idx_in_main:] + reversed_order[:idx_in_main]

    for i in order:
        cung_td = cung_tds[i]
        ten_cung = to_string(cung_td.select_one("p.text-sao-chinh-tinh").text)

        thang_el = cung_td.select("div.view-cung-dai-van > p")
        thang = to_string(thang_el[1].text) if len(thang_el) > 1 else ""

        sao = []

        chinh_tinh_els = cung_td.select("div.chinh-tinh p.text-chinh-chinh")
        for el in chinh_tinh_els:
            text = to_string(el.text.strip())
            if text:
                sao.append(text)

        sao_tot_divs = cung_td.select("div.sao-tot > div[data-sao-id]")
        for div in sao_tot_divs:
            classes = div.get("class", [])
            if "d-none" not in classes:
                text = to_string(div.text.strip())
                if text:
                    sao.append(text)

        sao_xau_divs = cung_td.select("div.sao-xau > div[data-sao-id]")
        for div in sao_xau_divs:
            classes = div.get("class", [])
            if "d-none" not in classes:
                text = to_string(div.text.strip())
                if text:
                    sao.append(text)

        bottom_el = cung_td.select_one("div.cung-bottom > span.txt-tiny-mid")
        if bottom_el:
            text = to_string(bottom_el.text.strip())
            if text:
                sao.append(text)

        data["cung"].append(schemas.CungDetail(ten=ten_cung, sao=sao, thang=thang))

    return data


def sort_cung_by_month(cung: list[schemas.CungDetail]):
    return list(sorted(cung, key=lambda x: int(x.thang.replace("Th.", ""))))


async def get_page_detail(
    dob: datetime,
    gender: str,
    full_name: str,
    nam_xem: Optional[int] = None,
) -> schemas.LaSoTuVi:
    context = await new_context()
    try:
        page = await context.new_page()
        await page.goto(URL)
        await page.wait_for_timeout(3000)

        # Scroll form into view
        breadcrumb = page.locator(".breadcrumb")
        if await breadcrumb.count() > 0:
            await breadcrumb.scroll_into_view_if_needed()

        # Name
        await page.locator('input[name="name"]').fill(full_name)

        # Day
        await page.locator(
            f"//select[@name='dayOfDOB']/option[text()='{dob.day}']"
        ).click()

        # Month
        await page.locator(
            f"//select[@name='monthOfDOB']/option[text()='Tháng {dob.month}']"
        ).click()

        # Year
        year_input = page.locator('input[name="yearOfDOB"]')
        await year_input.clear()
        await year_input.fill(str(dob.year))

        # Hour
        await page.locator(
            f"//select[@name='hourOfDOB']/option[text()='{dob.hour} Giờ']"
        ).click()

        # Minute
        await page.locator(
            f"//select[@name='minOfDOB']/option[text()='{dob.minute} Phút']"
        ).click()

        # Calendar: Dương lịch (first radio)
        calendar_radios = page.locator('input[name="calendar"]')
        if await calendar_radios.count() > 0:
            await calendar_radios.first.click()

        # Gender
        gender_radios = page.locator('input[name="gender"]')
        if gender == "Nam" and await gender_radios.count() > 0:
            await gender_radios.first.click()
        elif await gender_radios.count() > 1:
            await gender_radios.nth(1).click()

        # Năm xem
        if nam_xem is not None:
            try:
                await page.locator(
                    f"//select[@name='viewYear']/option[text()='{nam_xem}']"
                ).click(timeout=3000)
            except Exception:
                pass

        # Submit
        await page.locator(
            "//button[@type='submit' and contains(text(), 'Lập lá số')]"
        ).click()

        # Wait for result
        try:
            await page.wait_for_selector("td.cung", timeout=15000)
        except Exception:
            pass

        await page.wait_for_timeout(2000)
        body = await page.content()
        data = parse_body(body)

        la_so = schemas.LaSoTuVi(
            ngay_sinh=dob.strftime("%Y-%m-%d"),
            gio_sinh=dob.strftime("%H:%M"),
            gender=gender,
            am_duong=data["am_duong"],
            menh=data.get("menh"),
            menh_chu=data.get("menh_chu"),
            than_chu=data.get("than_chu"),
            cung=schemas.CungInfo(
                cung_chung=data["cung"],
                cung_10yrs=[],
                cung_12months=sort_cung_by_month(data["cung"]),
            ),
        )
        return la_so
    finally:
        await context.close()
