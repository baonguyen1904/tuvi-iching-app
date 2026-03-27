from pathlib import Path

import pytest
from app.services.scoring import ScoringEngine
from app.models.schemas import ScorePoint

XLSX_PATH = str(Path(__file__).resolve().parents[2] / "data" / "laso_points.xlsx")


@pytest.fixture(scope="module")
def engine():
    return ScoringEngine(xlsx_path=XLSX_PATH)


def test_calc_final_formula(engine):
    """final_pos = (raw + anchor) / 2, tb = pos + neg."""
    raws = {
        "cung_a": (10.0, -4.0),
        "cung_b": (6.0, -2.0),
    }
    anchor = (8.0, -3.0)
    periods = ["P1", "P2"]
    cung_order = ["cung_a", "cung_b"]

    points = engine._calc_final(raws, anchor, periods, cung_order)

    assert len(points) == 2

    # cung_a: final_pos = (10 + 8) / 2 = 9.0, final_neg = (-4 + -3) / 2 = -3.5
    assert abs(points[0].duong - 9.0) < 0.001
    assert abs(points[0].am - (-3.5)) < 0.001
    assert abs(points[0].tb - 5.5) < 0.001
    assert points[0].period == "P1"

    # cung_b: final_pos = (6 + 8) / 2 = 7.0, final_neg = (-2 + -3) / 2 = -2.5
    assert abs(points[1].duong - 7.0) < 0.001
    assert abs(points[1].am - (-2.5)) < 0.001
    assert abs(points[1].tb - 4.5) < 0.001
    assert points[1].period == "P2"


def test_calc_final_tb_is_algebraic_sum(engine):
    """tb = duong + am, NOT average."""
    raws = {"c": (20.0, -10.0)}
    anchor = (0.0, 0.0)
    points = engine._calc_final(raws, anchor, ["X"], ["c"])

    # duong = (20 + 0) / 2 = 10, am = (-10 + 0) / 2 = -5, tb = 10 + (-5) = 5
    assert abs(points[0].tb - (points[0].duong + points[0].am)) < 0.001
    assert abs(points[0].tb - 5.0) < 0.001


def test_calc_final_missing_cung_returns_anchor_only(engine):
    """If a cung is not in raws, raw = (0, 0), so final = anchor / 2."""
    raws = {}
    anchor = (10.0, -6.0)
    points = engine._calc_final(raws, anchor, ["P1"], ["missing_cung"])

    assert abs(points[0].duong - 5.0) < 0.001
    assert abs(points[0].am - (-3.0)) < 0.001


def test_summary_score_weighted_average(engine):
    """Summary = weighted average of tb using SUMMARY_AGE_WEIGHTS."""
    # All tb = 10.0 -> summary should be 10.0 regardless of weights
    points = [ScorePoint(period=f"{age}-{age+10}", duong=15.0, am=-5.0, tb=10.0)
              for age in range(0, 120, 10)]

    summary = engine._summary_score(points)
    assert abs(summary - 10.0) < 0.001


def test_summary_score_prime_years_weighted_higher(engine):
    """Prime years (20-60) should dominate when their values differ from others."""
    points = []
    for age in range(0, 120, 10):
        if 20 <= age <= 60:
            tb = 20.0  # high for prime years
        else:
            tb = 0.0   # zero for non-prime
        points.append(ScorePoint(period=f"{age}-{age+10}", duong=tb, am=0.0, tb=tb))

    summary = engine._summary_score(points)
    # Prime years dominate -> summary should be closer to 20 than to 0
    assert summary > 10.0


def test_summary_score_12_points_required(engine):
    """Must handle exactly 12 points (matching SUMMARY_AGE_WEIGHTS keys)."""
    points = [ScorePoint(period=f"{age}-{age+10}", duong=5.0, am=-2.0, tb=3.0)
              for age in range(0, 120, 10)]
    assert len(points) == 12

    summary = engine._summary_score(points)
    assert abs(summary - 3.0) < 0.001
