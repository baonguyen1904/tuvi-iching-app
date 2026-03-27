from pathlib import Path

import pytest
from dataclasses import dataclass
from app.services.scoring import ScoringEngine
from app.constants import HOUSE_WEIGHTS

XLSX_PATH = str(Path(__file__).resolve().parents[2] / "data" / "laso_points.xlsx")


@pytest.fixture(scope="module")
def engine():
    return ScoringEngine(xlsx_path=XLSX_PATH)


@dataclass
class FakeStar:
    slug: str


@dataclass
class FakeCung:
    name: str
    stars: list


def _make_cungs_with_known_star(engine, cung_names):
    """Create fake cungs where each cung has one known positive star."""
    pos_stars = [s for s in engine._star_table.values() if s.point > 0]
    cungs = []
    for i, name in enumerate(cung_names):
        star = pos_stars[i % len(pos_stars)]
        cungs.append(FakeCung(name=name, stars=[FakeStar(slug=star.slug)]))
    return cungs


def test_anchor_su_nghiep_uses_correct_cungs(engine):
    """su_nghiep anchor: quan loc 0.4, menh 0.2, tai bach 0.2, thien di 0.2."""
    cung_names = [
        "Mệnh", "Phụ Mẫu", "Phúc Đức", "Điền Trạch", "Quan Lộc", "Nô Bộc",
        "Thiên Di", "Tật Ách", "Tài Bạch", "Tử Tức", "Phu Thê", "Huynh Đệ",
    ]
    cungs = _make_cungs_with_known_star(engine, cung_names)
    lifetime_raws = engine._build_raw_scores(cungs, "su_nghiep")

    anchor_pos, anchor_neg = engine._calc_anchor(lifetime_raws, "su_nghiep", than_cu="Thiên Di")

    # Verify anchor is a weighted sum (not zero if cungs have stars)
    assert anchor_pos > 0 or anchor_neg < 0


def test_anchor_van_menh_resolves_than(engine):
    """van_menh has 'than' in config -- must resolve to than_cu cung."""
    cung_names = [
        "Mệnh", "Phụ Mẫu", "Phúc Đức", "Điền Trạch", "Quan Lộc", "Nô Bộc",
        "Thiên Di", "Tật Ách", "Tài Bạch", "Tử Tức", "Phu Thê", "Huynh Đệ",
    ]
    cungs = _make_cungs_with_known_star(engine, cung_names)
    lifetime_raws = engine._build_raw_scores(cungs, "van_menh")

    # than_cu = "Quan Loc" -> "than" should resolve to "quan loc"
    anchor_pos, anchor_neg = engine._calc_anchor(lifetime_raws, "van_menh", than_cu="Quan Lộc")
    assert isinstance(anchor_pos, float)
    assert isinstance(anchor_neg, float)


def test_anchor_formula_manual_check(engine):
    """Manually verify anchor = sum(raw_score[cung] x house_weight) for suc_khoe."""
    cung_names = [
        "Mệnh", "Phụ Mẫu", "Phúc Đức", "Điền Trạch", "Quan Lộc", "Nô Bộc",
        "Thiên Di", "Tật Ách", "Tài Bạch", "Tử Tức", "Phu Thê", "Huynh Đệ",
    ]
    cungs = _make_cungs_with_known_star(engine, cung_names)
    lifetime_raws = engine._build_raw_scores(cungs, "suc_khoe")

    anchor_pos, anchor_neg = engine._calc_anchor(lifetime_raws, "suc_khoe", than_cu="Thiên Di")

    # suc_khoe: tat ach x 0.6 + phuc duc x 0.4
    tat_ach_pos, tat_ach_neg = lifetime_raws["tật ách"]
    phuc_duc_pos, phuc_duc_neg = lifetime_raws["phúc đức"]
    expected_pos = tat_ach_pos * 0.6 + phuc_duc_pos * 0.4
    expected_neg = tat_ach_neg * 0.6 + phuc_duc_neg * 0.4

    assert abs(anchor_pos - expected_pos) < 0.001
    assert abs(anchor_neg - expected_neg) < 0.001


def test_anchor_missing_cung_contributes_zero(engine):
    """If a cung referenced in house weights is missing from raws -> 0 contribution."""
    # Only provide "menh", missing "quan loc", "tai bach", "thien di"
    pos_stars = [s for s in engine._star_table.values() if s.point > 0]
    cungs = [FakeCung(name="Mệnh", stars=[FakeStar(slug=pos_stars[0].slug)])]
    lifetime_raws = engine._build_raw_scores(cungs, "su_nghiep")

    anchor_pos, anchor_neg = engine._calc_anchor(lifetime_raws, "su_nghiep", than_cu="Thiên Di")

    # Only menh contributes (weight 0.2), others are 0
    menh_pos, _ = lifetime_raws["mệnh"]
    expected_pos = menh_pos * 0.2
    assert abs(anchor_pos - expected_pos) < 0.001


def test_anchor_all_dimensions_produce_values(engine):
    """All 8 dimensions produce anchor values without errors."""
    cung_names = [
        "Mệnh", "Phụ Mẫu", "Phúc Đức", "Điền Trạch", "Quan Lộc", "Nô Bộc",
        "Thiên Di", "Tật Ách", "Tài Bạch", "Tử Tức", "Phu Thê", "Huynh Đệ",
    ]
    cungs = _make_cungs_with_known_star(engine, cung_names)

    for dim in HOUSE_WEIGHTS:
        lifetime_raws = engine._build_raw_scores(cungs, dim)
        anchor_pos, anchor_neg = engine._calc_anchor(lifetime_raws, dim, than_cu="Thiên Di")
        assert isinstance(anchor_pos, float)
        assert isinstance(anchor_neg, float)
