import json

import pytest

from app.services.scraper_cohoc import get_gio_sinh_option, parse_body


class TestGetGioSinhOption:
    def test_midnight(self):
        from datetime import datetime
        assert get_gio_sinh_option(datetime(2000, 1, 1, 0, 0)) == 1

    def test_hour_23(self):
        from datetime import datetime
        assert get_gio_sinh_option(datetime(2000, 1, 1, 23, 0)) == 1

    def test_hour_1(self):
        from datetime import datetime
        assert get_gio_sinh_option(datetime(2000, 1, 1, 1, 0)) == 1

    def test_hour_7(self):
        from datetime import datetime
        assert get_gio_sinh_option(datetime(2000, 1, 1, 7, 0)) == 5

    def test_hour_12(self):
        from datetime import datetime
        assert get_gio_sinh_option(datetime(2000, 1, 1, 12, 0)) == 7

    def test_hour_21(self):
        from datetime import datetime
        assert get_gio_sinh_option(datetime(2000, 1, 1, 21, 0)) == 12


class TestParseBody:
    def test_parse_produces_12_cungs(self, cohoc_html):
        data = parse_body(cohoc_html)
        assert len(data["cung"]) == 12

    def test_parse_first_cung_is_menh(self, cohoc_html):
        data = parse_body(cohoc_html)
        assert "MỆNH" in data["cung"][0]["ten"].upper() or "Mệnh" in data["cung"][0]["ten"]

    def test_parse_each_cung_has_stars(self, cohoc_html):
        data = parse_body(cohoc_html)
        for cung in data["cung"]:
            assert len(cung["sao"]) >= 1, f"Cung '{cung['ten']}' has no stars"

    def test_parse_metadata_present(self, cohoc_html):
        data = parse_body(cohoc_html)
        assert data.get("am_duong") is not None

    def test_parse_10yr_cungs(self, cohoc_html):
        data = parse_body(cohoc_html)
        assert len(data["cung_10yrs"]) == 12


@pytest.mark.live
class TestLiveCohoc:
    """Live integration tests — run with: pytest -m live"""

    @pytest.fixture
    def _browser(self):
        import asyncio
        from app.services import scraper_browser

        async def setup():
            await scraper_browser.start()

        asyncio.get_event_loop().run_until_complete(setup())
        yield
        asyncio.get_event_loop().run_until_complete(scraper_browser.shutdown())

    def test_determinism(self, _browser):
        """Same input twice produces identical output."""
        import asyncio
        from datetime import datetime
        from app.services.scraper_cohoc import get_page_detail

        async def run():
            dob = datetime(1997, 10, 11)
            result1 = await get_page_detail(dob, 12, "Nam")
            result2 = await get_page_detail(dob, 12, "Nam")
            return result1, result2

        r1, r2 = asyncio.get_event_loop().run_until_complete(run())
        assert r1["cung"] == r2["cung"]
