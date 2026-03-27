import logging
import re
from datetime import datetime

from bs4 import BeautifulSoup

from app.services import constants, soup_utils
from app.services.scraper_browser import new_context

logger = logging.getLogger(__name__)

GIO_SINH = constants.GIO_SINH

# Container selector for metadata — tuvi.vn uses div.view-thien-ban
_META_CONTAINER = "div.view-thien-ban"


def get_gio_sinh_option(time: datetime):
    for k, v in GIO_SINH.items():
        if time.hour in [23, 24, 0, 1]:
            return 1

        start, end = v
        if start <= time.hour < end:
            return k


def _get_cung_name(cung_td):
    """Extract cung name from a <td class='cung'> element."""
    el = cung_td.select_one("p.text-sao-chinh-tinh")
    if el:
        return el.text.strip()
    # Fallback: use data attribute
    return cung_td.get("data-cung-full-name", "").strip()


def _get_cung_stars(cung_td):
    """Extract all stars for a cung, preserving order: chinh tinh, sao tot, sao xau, bottom."""
    sao = []

    # Chinh tinh (main stars)
    for p in cung_td.select("p.text-chinh-chinh"):
        txt = p.text.strip()
        if txt:
            sao.append(txt)

    # Sao tot (auspicious stars) — skip hidden d-none elements
    for div in cung_td.select("div.sao-tot div.text-sao-xau-tot"):
        classes = div.get("class", [])
        if "d-none" not in classes:
            txt = div.text.strip()
            if txt:
                sao.append(txt)

    # Sao xau (inauspicious stars) — skip hidden d-none elements
    for div in cung_td.select("div.sao-xau div.text-sao-xau-tot"):
        classes = div.get("class", [])
        if "d-none" not in classes:
            txt = div.text.strip()
            if txt:
                sao.append(txt)

    # Bottom span (tieu-van or transcient star)
    bottom_div = cung_td.select_one("div.cung-bottom")
    if bottom_div:
        for span in bottom_div.select("span"):
            cls = span.get("class", [])
            # Skip luu-nien spans (LN.*) — only include dai-van text-tieu-van
            if "text-tieu-van" in cls:
                txt = span.text.strip()
                if txt:
                    sao.append(txt)

    # Fallback: if no stars found, try legacy ul.sao-tot / ul.sao-xau (cohoc.net style)
    if not sao:
        for li in cung_td.select("ul.sao-tot > li, ul.sao-xau > li"):
            txt = li.text.strip()
            if txt:
                sao.append(txt)
        legacy_bottom = cung_td.select_one("div.cung-bottom > p > span")
        if legacy_bottom:
            sao.append(legacy_bottom.text.strip())

    return sao


def _get_tieuvan_year(cung_td):
    """Extract tiểu vận year (lunar year) from a cung td."""
    # tuvi.vn: div[class*=khoi-tieu-han] > span
    khoi = cung_td.select_one("div[class*='khoi-tieu-han']")
    if khoi:
        span = khoi.select_one("span")
        if span:
            return span.text.strip()
    # Fallback: cohoc.net uses span.cung-tieuvan
    tieuvan = cung_td.select_one("span.cung-tieuvan")
    if tieuvan:
        return tieuvan.text.strip()
    return None


def _build_cung_list(cung_tds, start_idx, am_duong, use_gender_for_10yr=False):
    """Return ordered list of cung dicts starting from the given index."""
    main_order = constants.MAIN_ORDER
    reversed_order = constants.REVERSED_ORDER

    if use_gender_for_10yr:
        # 10yr ordering: Nam = main, Nữ = reversed
        if "Nam" in am_duong:
            idx_in_order = main_order.index(start_idx)
            order = main_order[idx_in_order:] + main_order[:idx_in_order]
        else:
            idx_in_order = reversed_order.index(start_idx)
            order = reversed_order[idx_in_order:] + reversed_order[:idx_in_order]
    else:
        # Lifetime ordering: Dương Nam / Âm Nữ = main, others = reversed
        if am_duong in ["Dương Nam", "Âm Nữ"]:
            idx_in_order = main_order.index(start_idx)
            order = main_order[idx_in_order:] + main_order[:idx_in_order]
        else:
            idx_in_order = reversed_order.index(start_idx)
            order = reversed_order[idx_in_order:] + reversed_order[:idx_in_order]

    result = []
    for i in order:
        cung_td = cung_tds[i]
        ten_cung = _get_cung_name(cung_td)
        sao = _get_cung_stars(cung_td)
        result.append({"ten": ten_cung, "sao": sao})
    return result


def parse_body(body):
    soup = BeautifulSoup(body, features="html.parser")

    # Detect container selector (tuvi.vn vs cohoc.net)
    if soup.select_one(_META_CONTAINER):
        meta_container = _META_CONTAINER
    else:
        meta_container = "div.thien-ban"

    data = {
        "nam": soup_utils.find_metadata_field(soup, "Năm:", container_selector=meta_container),
        "menh": soup_utils.find_metadata_field(
            soup, "Bản mệnh:", container_selector=meta_container
        ),
        "cuc": soup_utils.find_metadata_field(soup, "Cục:", container_selector=meta_container),
        "cung": [],
        "cung_10yrs": [],
    }

    data["than_cu"] = soup_utils.find_metadata_field(
        soup, "Lai\nnhân cung:", container_selector=meta_container
    ) or soup_utils.find_metadata_field(
        soup, "Thân cư:", container_selector=meta_container
    )
    data["menh_chu"] = soup_utils.find_metadata_field(
        soup, "Chủ mệnh:", container_selector=meta_container
    ) or soup_utils.find_metadata_field(
        soup, "Mệnh chủ:", container_selector=meta_container
    )
    data["than_chu"] = soup_utils.find_metadata_field(
        soup, "Chủ thân:", container_selector=meta_container
    ) or soup_utils.find_metadata_field(
        soup, "Thân chủ:", container_selector=meta_container
    )

    # Âm Dương — tuvi.vn uses "Âm dương:", cohoc.net uses "Âm Dương:"
    am_duong = soup_utils.find_metadata_field(
        soup, "Âm dương:", container_selector=meta_container
    ) or soup_utils.find_metadata_field(
        soup, "Âm Dương:", container_selector=meta_container
    )
    data["am_duong"] = am_duong

    # 12 Cung (lifetime)
    cung_tds = soup.select("td.cung")

    # Find MỆNH cung index
    start_idx = None
    for i, td in enumerate(cung_tds):
        name = _get_cung_name(td).upper()
        if "MỆ" in name or "ME" in name.upper():
            # Check if this is the Mệnh cung (not Phu Mẫu etc.)
            cung_id = td.get("id", "")
            if "menh" in cung_id and "phu-mau" not in cung_id:
                start_idx = i
                break
            # Fallback: cung name is exactly "Mệnh" or "MỆNH"
            raw_name = _get_cung_name(td)
            if raw_name.strip() in ["Mệnh", "MỆNH"]:
                start_idx = i
                break

    if start_idx is None:
        raise ValueError("Could not find MỆNH cung in HTML")

    data["cung"] = _build_cung_list(cung_tds, start_idx, am_duong, use_gender_for_10yr=False)

    # Vận 10 năm — find cung containing current lunar year
    today = datetime.now()
    current_luna_year = constants.LUNA_YEARS.get(today.year)
    if current_luna_year is None:
        logger.warning("No LUNA_YEARS entry for year %d", today.year)
        data["cung_10yrs"] = []
        return data

    tieuvan_start_idx = None
    for i, td in enumerate(cung_tds):
        year = _get_tieuvan_year(td)
        if year and year.strip() == current_luna_year:
            tieuvan_start_idx = i
            break

    if tieuvan_start_idx is None:
        logger.warning("Could not find lunar year '%s' in cung tieuvan", current_luna_year)
        data["cung_10yrs"] = []
        return data

    data["cung_10yrs"] = _build_cung_list(
        cung_tds, tieuvan_start_idx, am_duong, use_gender_for_10yr=True
    )

    return data


async def get_page_detail(dob: datetime, time, gender: str):
    context = await new_context()
    try:
        page = await context.new_page()
        await page.goto(constants.COHOC_FORM_URL)

        # Wait for form to be ready
        try:
            await page.wait_for_selector("#btGiaiDoan", timeout=15000)
        except Exception:
            raise RuntimeError("Form page did not load in time")

        # Fill form
        await page.locator(f"//select[@name='ddlNgay']/option[text()='{dob.day}']").click()
        await page.locator(f"//select[@name='ddlThang']/option[text()='{dob.month}']").click()
        await page.locator(f"//select[@name='ddlNam']/option[text()='{dob.year}']").click()
        await page.locator(f"//select[@name='ddlGio']/option[@value='{time}']").click()
        await page.locator(f"//input[@name='GioiTinh'][@value='rd{gender}']").click()

        # Submit
        await page.evaluate('document.getElementById("btGiaiDoan").click()')

        # Wait for navigation
        form_url = page.url
        try:
            await page.wait_for_url(lambda url: url != form_url, timeout=15000)
        except Exception:
            raise RuntimeError("Form did not navigate after submit")

        current_url = page.url

        # IP rate-limit
        if "ip-deny" in current_url or "no-refer-ip-deny" in current_url:
            raise RuntimeError(f"IP denied by tuvi.cohoc.net: {current_url}")

        # Cache-not-found: server generating, wait up to 90s
        if "cache-not-found" in current_url:
            logger.info("Processing page detected, waiting up to 90s...")
            try:
                await page.wait_for_selector("div.thien-ban", timeout=90000)
            except Exception:
                raise RuntimeError(
                    f"Timeout waiting for result after processing page. "
                    f"Server may still be generating cache for {dob.strftime('%d/%m/%Y')}."
                )
        else:
            try:
                await page.wait_for_selector("div.thien-ban", timeout=10000)
            except Exception:
                raise RuntimeError(f"Result page did not load: {current_url}")

        body = await page.content()
        data = parse_body(body)
        return data
    finally:
        await context.close()
