"""End-to-end integration test: scrape both sites, verify combined output.

Run with: pytest -m live tests/test_integration.py -v
"""
import asyncio

import pytest

from app.models.schemas import LaSoTuVi


@pytest.mark.live
class TestFullScrape:
    @pytest.fixture(autouse=True)
    def _browser(self):
        from app.services import scraper_browser

        asyncio.get_event_loop().run_until_complete(scraper_browser.start())
        yield
        asyncio.get_event_loop().run_until_complete(scraper_browser.shutdown())

    def test_cohoc_and_tuvivn_produce_valid_output(self):
        from datetime import datetime
        from app.services.scraper_cohoc import get_page_detail as cohoc_scrape
        from app.services.scraper_tuvivn import get_page_detail as tuvivn_scrape

        async def run():
            dob = datetime(1997, 10, 11)
            cohoc_data = await cohoc_scrape(dob, 12, "Nam")

            dob_vn = datetime(1997, 10, 11, 12, 0)
            tuvivn_data = await tuvivn_scrape(dob_vn, "Nam", "Test User", nam_xem=2026)

            return cohoc_data, tuvivn_data

        cohoc, tuvivn = asyncio.get_event_loop().run_until_complete(run())

        # cohoc: lifetime + 10yr
        assert len(cohoc["cung"]) == 12
        assert len(cohoc["cung_10yrs"]) == 12
        assert cohoc["am_duong"] is not None

        # tuvivn: monthly
        assert isinstance(tuvivn, LaSoTuVi)
        assert tuvivn.cung is not None
        assert len(tuvivn.cung.cung_12months) == 12
        for cung in tuvivn.cung.cung_12months:
            assert cung.thang is not None
