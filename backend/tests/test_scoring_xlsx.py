from pathlib import Path

import pytest
from app.services.scoring import ScoringEngine
from app.models.schemas import StarRow

XLSX_PATH = str(Path(__file__).resolve().parents[2] / "data" / "laso_points.xlsx")


@pytest.fixture(scope="module")
def engine():
    return ScoringEngine(xlsx_path=XLSX_PATH)


def test_star_table_loaded(engine):
    assert len(engine._star_table) > 200


def test_star_table_no_duplicates(engine):
    # 223 rows, 2 known duplicates -> expect >= 221 unique
    assert len(engine._star_table) >= 221


def test_star_row_structure(engine):
    # Pick a known star -- "TU VI (B)" should always exist
    from slugify import slugify
    slug = slugify("TỬ VI (B)".lower())
    row = engine._star_table.get(slug)
    assert row is not None
    assert isinstance(row, StarRow)
    assert isinstance(row.point, int)
    assert isinstance(row.weights, dict)
    assert "su_nghiep" in row.weights


def test_empty_weight_defaults_to_one(engine):
    """van_menh column is all NaN -> all stars should have weight 1.0."""
    for slug, row in engine._star_table.items():
        assert row.weights["van_menh"] == 1.0, (
            f"Star {row.name} has van_menh weight {row.weights['van_menh']}, expected 1.0"
        )


def test_point_range(engine):
    for slug, row in engine._star_table.items():
        assert -5 <= row.point <= 10, f"Star {row.name} has point {row.point} out of range"


def test_pct_fvg_values(engine):
    valid_values = {"pos", "neg", None}
    for slug, row in engine._star_table.items():
        for level in (30, 50):
            val = row.pct_fvg.get(level)
            assert val in valid_values, f"Star {row.name} pct_fvg_{level} = {val}"


def test_alert_tags_structure(engine):
    """Stars with pct_fvg should have corresponding tag columns."""
    found_any_tag = False
    for slug, row in engine._star_table.items():
        for dim in ["su_nghiep", "tien_bac", "hon_nhan", "suc_khoe", "dat_dai", "hoc_tap", "con_cai"]:
            for level in (30, 50):
                tag = row.alert_tags.get(dim, {}).get(level)
                if tag is not None:
                    found_any_tag = True
                    assert isinstance(tag, str)
                    assert len(tag) > 0
    assert found_any_tag, "No alert tags found in any star"
