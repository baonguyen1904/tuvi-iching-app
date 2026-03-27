from pathlib import Path

import pytest
from dataclasses import dataclass
from app.services.scoring import ScoringEngine
from app.models.schemas import StarRow

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


def test_raw_scores_positive_stars(engine):
    """Cung with only positive-point stars -> raw_pos > 0, raw_neg == 0."""
    pos_stars = [s for s in engine._star_table.values() if s.point > 0]
    assert len(pos_stars) > 0
    star = pos_stars[0]

    cungs = [FakeCung(name="test_cung", stars=[FakeStar(slug=star.slug)])]
    raws = engine._build_raw_scores(cungs, "su_nghiep")

    assert "test_cung" in raws
    raw_pos, raw_neg = raws["test_cung"]
    assert raw_pos > 0
    assert raw_neg == 0.0


def test_raw_scores_negative_stars(engine):
    """Cung with only negative-point stars -> raw_pos == 0, raw_neg < 0."""
    neg_stars = [s for s in engine._star_table.values() if s.point < 0]
    assert len(neg_stars) > 0
    star = neg_stars[0]

    cungs = [FakeCung(name="test_cung", stars=[FakeStar(slug=star.slug)])]
    raws = engine._build_raw_scores(cungs, "su_nghiep")

    raw_pos, raw_neg = raws["test_cung"]
    assert raw_pos == 0.0
    assert raw_neg < 0


def test_raw_scores_zero_point_goes_to_neg(engine):
    """Stars with point == 0 contribute to neg bucket (point <= 0)."""
    zero_stars = [s for s in engine._star_table.values() if s.point == 0]
    if not zero_stars:
        pytest.skip("No zero-point stars in dataset")
    star = zero_stars[0]

    cungs = [FakeCung(name="test_cung", stars=[FakeStar(slug=star.slug)])]
    raws = engine._build_raw_scores(cungs, "su_nghiep")

    raw_pos, raw_neg = raws["test_cung"]
    # 0 * weight = 0, so both should be 0
    assert raw_pos == 0.0
    assert raw_neg == 0.0


def test_raw_scores_formula_point_times_weight(engine):
    """Verify raw = point x weight for a known star."""
    from slugify import slugify
    slug = slugify("TỬ VI (B)".lower())
    star_row = engine._star_table[slug]

    cungs = [FakeCung(name="cung_a", stars=[FakeStar(slug=slug)])]
    raws = engine._build_raw_scores(cungs, "su_nghiep")

    raw_pos, raw_neg = raws["cung_a"]
    expected = star_row.point * star_row.weights["su_nghiep"]
    if star_row.point > 0:
        assert abs(raw_pos - expected) < 0.001
        assert raw_neg == 0.0
    else:
        assert raw_pos == 0.0
        assert abs(raw_neg - expected) < 0.001


def test_raw_scores_van_menh_uses_weight_one(engine):
    """van_menh column is all NaN -> weight defaults to 1.0, so raw = point x 1."""
    from slugify import slugify
    slug = slugify("TỬ VI (B)".lower())
    star_row = engine._star_table[slug]

    cungs = [FakeCung(name="cung_a", stars=[FakeStar(slug=slug)])]
    raws = engine._build_raw_scores(cungs, "van_menh")

    raw_pos, raw_neg = raws["cung_a"]
    expected = star_row.point * 1.0  # weight should be 1.0
    if star_row.point > 0:
        assert abs(raw_pos - expected) < 0.001


def test_raw_scores_unknown_star_skipped(engine):
    """Unknown star slug -> skipped with no error."""
    cungs = [FakeCung(name="cung_a", stars=[FakeStar(slug="nonexistent-star-xyz")])]
    raws = engine._build_raw_scores(cungs, "su_nghiep")
    raw_pos, raw_neg = raws["cung_a"]
    assert raw_pos == 0.0
    assert raw_neg == 0.0


def test_raw_scores_multiple_cungs(engine):
    """Multiple cungs each get their own entry."""
    stars = [s for s in engine._star_table.values() if s.point > 0][:2]
    cungs = [
        FakeCung(name="mệnh", stars=[FakeStar(slug=stars[0].slug)]),
        FakeCung(name="quan lộc", stars=[FakeStar(slug=stars[1].slug)]),
    ]
    raws = engine._build_raw_scores(cungs, "su_nghiep")
    assert "mệnh" in raws
    assert "quan lộc" in raws


def test_raw_scores_cung_name_lowered(engine):
    """Cung names are lowered in the output dict keys."""
    stars = [s for s in engine._star_table.values() if s.point > 0][:1]
    cungs = [FakeCung(name="Mệnh", stars=[FakeStar(slug=stars[0].slug)])]
    raws = engine._build_raw_scores(cungs, "su_nghiep")
    assert "mệnh" in raws
    assert "Mệnh" not in raws
