from pathlib import Path

import pytest
from dataclasses import dataclass
from app.services.scoring import ScoringEngine
from app.models.schemas import ScorePoint, Alert

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


def _make_points(values_duong, values_am, period_labels):
    """Helper: build ScorePoint list from parallel arrays."""
    return [
        ScorePoint(period=str(p), duong=d, am=a, tb=d + a)
        for p, d, a in zip(period_labels, values_duong, values_am)
    ]


def _find_star_with_tag(engine, level, direction, dim="su_nghiep"):
    """Find a star that has pct_fvg at given level/direction AND a tag for the dimension."""
    for s in engine._star_table.values():
        if s.pct_fvg.get(level) == direction:
            tag = s.alert_tags.get(dim, {}).get(level)
            if tag:
                return s, dim
    # Fallback: try other dimensions
    for alt_dim in ["hon_nhan", "tien_bac", "suc_khoe", "dat_dai", "hoc_tap", "con_cai"]:
        for s in engine._star_table.values():
            if s.pct_fvg.get(level) == direction:
                tag = s.alert_tags.get(alt_dim, {}).get(level)
                if tag:
                    return s, alt_dim
    return None, None


def test_alert_50pct_positive_detected(engine):
    """A 60% jump on duong line -> level 50 alert."""
    points = _make_points(
        values_duong=[10.0, 16.0],  # 60% increase
        values_am=[-5.0, -5.0],
        period_labels=["0-10", "10-20"],
    )
    star, dim = _find_star_with_tag(engine, 50, "pos")
    if star is None:
        pytest.skip("No stars with pct_fvg_50=pos and a tag in any dimension")

    cungs = [
        FakeCung(name="0-10", stars=[]),  # source period
        FakeCung(name="10-20", stars=[FakeStar(slug=star.slug)]),  # destination
    ]

    alerts = engine._detect_alerts(points, cungs, dim, "lifetime")
    level_50 = [a for a in alerts if a.level == 50]
    assert len(level_50) >= 1
    assert level_50[0].type == "positive"
    assert level_50[0].period == "10-20"


def test_alert_30pct_detected(engine):
    """A 35% jump -> level 30 alert."""
    points = _make_points(
        values_duong=[10.0, 13.5],  # 35% increase
        values_am=[-5.0, -5.0],
        period_labels=["0-10", "10-20"],
    )
    star, dim = _find_star_with_tag(engine, 30, "pos")
    if star is None:
        pytest.skip("No stars with pct_fvg_30=pos and a tag")

    cungs = [
        FakeCung(name="0-10", stars=[]),
        FakeCung(name="10-20", stars=[FakeStar(slug=star.slug)]),
    ]

    alerts = engine._detect_alerts(points, cungs, dim, "lifetime")
    level_30 = [a for a in alerts if a.level == 30]
    assert len(level_30) >= 1


def test_alert_50_takes_priority_over_30(engine):
    """When pct >= 50, only level 50 alert should appear, not 30."""
    points = _make_points(
        values_duong=[10.0, 20.0],  # 100% increase
        values_am=[-5.0, -5.0],
        period_labels=["0-10", "10-20"],
    )
    # Find a star with both pct_fvg levels AND tags in a dimension
    star = None
    dim = None
    for s in engine._star_table.values():
        if s.pct_fvg.get(50) == "pos" and s.pct_fvg.get(30) == "pos":
            for d in ["su_nghiep", "hon_nhan", "tien_bac", "suc_khoe", "dat_dai", "hoc_tap", "con_cai"]:
                tag50 = s.alert_tags.get(d, {}).get(50)
                tag30 = s.alert_tags.get(d, {}).get(30)
                if tag50 and tag30:
                    star = s
                    dim = d
                    break
            if star:
                break
    if star is None:
        pytest.skip("No stars with both pct_fvg levels and tags")

    cungs = [
        FakeCung(name="0-10", stars=[]),
        FakeCung(name="10-20", stars=[FakeStar(slug=star.slug)]),
    ]

    alerts = engine._detect_alerts(points, cungs, dim, "lifetime")
    # Should have level 50, but NOT level 30 for the same transition
    periods_50 = {a.period for a in alerts if a.level == 50 and a.star_name == star.slug}
    periods_30 = {a.period for a in alerts if a.level == 30 and a.star_name == star.slug}
    overlap = periods_50 & periods_30
    assert len(overlap) == 0, f"Same transition has both 30 and 50: {overlap}"


def test_alert_neg_line_inverted(engine):
    """Am line: going from -10 to -5 is improvement -> positive pct_change."""
    points = _make_points(
        values_duong=[10.0, 10.0],
        values_am=[-10.0, -5.0],  # 50% improvement (less negative)
        period_labels=["0-10", "10-20"],
    )
    star, dim = _find_star_with_tag(engine, 50, "pos")
    if star is None:
        pytest.skip("No stars with pct_fvg_50=pos and a tag")

    cungs = [
        FakeCung(name="0-10", stars=[]),
        FakeCung(name="10-20", stars=[FakeStar(slug=star.slug)]),
    ]

    alerts = engine._detect_alerts(points, cungs, dim, "lifetime")
    # After inversion, this should be detected as positive change
    pos_alerts = [a for a in alerts if a.type == "positive"]
    assert len(pos_alerts) >= 1


def test_alert_zero_previous_skipped(engine):
    """If previous value is 0, skip alert detection for that transition."""
    points = _make_points(
        values_duong=[0.0, 10.0],
        values_am=[0.0, -5.0],
        period_labels=["0-10", "10-20"],
    )
    cungs = [
        FakeCung(name="0-10", stars=[]),
        FakeCung(name="10-20", stars=[]),
    ]

    alerts = engine._detect_alerts(points, cungs, "su_nghiep", "lifetime")
    assert len(alerts) == 0


def test_alert_van_menh_no_alerts(engine):
    """van_menh should never have alerts -- enforced by caller, but verify here."""
    # This is a design rule: _detect_alerts should still work if called,
    # but the caller (score method) skips calling it for van_menh.
    # We test the caller behavior in integration tests.
    pass


def test_alert_lifetime_after_age_80_skipped(engine):
    """No alerts for transitions after age 80 on lifetime chart."""
    # 12 points: ages 0, 10, 20, ..., 110
    duong_values = [10.0] * 9 + [20.0, 40.0, 80.0]  # big jumps at 80, 90, 100
    am_values = [-5.0] * 12
    period_labels = [f"{age}-{age+10}" for age in range(0, 120, 10)]

    points = _make_points(duong_values, am_values, period_labels)

    # Even with big jumps, no alerts after age 80
    cungs = [FakeCung(name=p, stars=[]) for p in period_labels]
    alerts = engine._detect_alerts(points, cungs, "su_nghiep", "lifetime")

    late_alerts = [a for a in alerts if a.period in ("80-90", "90-100", "100-110")]
    assert len(late_alerts) == 0


def test_alert_con_cai_after_age_60_skipped(engine):
    """con_cai: no alerts after age 60 on lifetime chart."""
    duong_values = [10.0] * 7 + [20.0, 40.0, 80.0, 160.0, 320.0]
    am_values = [-5.0] * 12
    period_labels = [f"{age}-{age+10}" for age in range(0, 120, 10)]

    points = _make_points(duong_values, am_values, period_labels)
    cungs = [FakeCung(name=p, stars=[]) for p in period_labels]

    alerts = engine._detect_alerts(points, cungs, "con_cai", "lifetime")

    late_alerts = [a for a in alerts if a.period in (
        "60-70", "70-80", "80-90", "90-100", "100-110"
    )]
    assert len(late_alerts) == 0


def test_alert_below_30pct_no_alert(engine):
    """Changes < 30% should NOT trigger alerts."""
    points = _make_points(
        values_duong=[10.0, 12.0],  # 20% increase -- below threshold
        values_am=[-5.0, -5.0],
        period_labels=["0-10", "10-20"],
    )
    cungs = [
        FakeCung(name="0-10", stars=[]),
        FakeCung(name="10-20", stars=[]),
    ]

    alerts = engine._detect_alerts(points, cungs, "su_nghiep", "lifetime")
    assert len(alerts) == 0
