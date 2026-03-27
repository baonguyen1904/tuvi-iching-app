import pytest

from app.models.schemas import CungDetail
from app.services.scraper_tuvivn import parse_body, sort_cung_by_month, to_string


class TestToString:
    def test_basic_cleanup(self):
        assert to_string("  Tử   Vi  ") == "Tử Vi"

    def test_removes_dashes(self):
        assert to_string("Thiên - Đồng") == "Thiên Đồng"

    def test_removes_plus(self):
        assert to_string("Sao +Tot") == "Sao Tot"


class TestSortCungByMonth:
    def test_sorts_by_month_number(self):
        cungs = [
            CungDetail(ten="B", sao=[], thang="Th.3"),
            CungDetail(ten="A", sao=[], thang="Th.1"),
            CungDetail(ten="C", sao=[], thang="Th.12"),
        ]
        result = sort_cung_by_month(cungs)
        assert [c.thang for c in result] == ["Th.1", "Th.3", "Th.12"]


class TestParseBody:
    def test_parse_produces_12_cungs(self, tuvivn_html):
        data = parse_body(tuvivn_html)
        assert len(data["cung"]) == 12

    def test_each_cung_has_stars(self, tuvivn_html):
        data = parse_body(tuvivn_html)
        for cung in data["cung"]:
            assert len(cung.sao) >= 1, f"Cung '{cung.ten}' has no stars"

    def test_each_cung_has_month(self, tuvivn_html):
        data = parse_body(tuvivn_html)
        for cung in data["cung"]:
            assert cung.thang is not None and cung.thang != ""

    def test_menh_is_first_cung(self, tuvivn_html):
        data = parse_body(tuvivn_html)
        assert "Mệnh" in data["cung"][0].ten or "mệnh" in data["cung"][0].ten.lower()

    def test_metadata_am_duong(self, tuvivn_html):
        data = parse_body(tuvivn_html)
        assert data.get("am_duong") is not None


@pytest.mark.live
class TestLiveTuViVn:
    """Live integration tests — run with: pytest -m live"""

    def test_determinism(self):
        import asyncio
        from datetime import datetime
        from app.services import scraper_browser
        from app.services.scraper_tuvivn import get_page_detail

        async def run():
            await scraper_browser.start()
            try:
                dob = datetime(1997, 10, 11, 12, 0)
                r1 = await get_page_detail(dob, "Nam", "Test", nam_xem=2026)
                r2 = await get_page_detail(dob, "Nam", "Test", nam_xem=2026)
                return r1, r2
            finally:
                await scraper_browser.shutdown()

        r1, r2 = asyncio.get_event_loop().run_until_complete(run())
        assert r1.cung.cung_12months == r2.cung.cung_12months
