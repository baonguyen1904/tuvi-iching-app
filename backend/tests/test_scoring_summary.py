from pathlib import Path

import pytest
from app.services.scoring import ScoringEngine
from app.models.schemas import ScorePoint
from app.constants import SUMMARY_AGE_WEIGHTS

XLSX_PATH = str(Path(__file__).resolve().parents[2] / "data" / "laso_points.xlsx")


@pytest.fixture(scope="module")
def engine():
    return ScoringEngine(xlsx_path=XLSX_PATH)


def _make_lifetime(tb_values):
    """Build 12-point lifetime list from tb values."""
    ages = list(range(0, 120, 10))
    return [
        ScorePoint(period=f"{a}-{a+10}", duong=max(tb, 0), am=min(tb, 0), tb=tb)
        for a, tb in zip(ages, tb_values)
    ]


def test_uniform_tb_returns_same_value(engine):
    points = _make_lifetime([7.0] * 12)
    assert abs(engine._summary_score(points) - 7.0) < 0.01


def test_prime_years_dominate(engine):
    """If prime years (20-60) are 100 and rest are 0, summary > 50."""
    tb_values = [0, 0, 100, 100, 100, 100, 100, 0, 0, 0, 0, 0]
    summary = engine._summary_score(_make_lifetime(tb_values))
    # Weighted: 5 * 1.5 * 100 = 750, total weight = 2*0.5 + 5*1.5 + 3*1.0 + 2*0.5 = 12.5
    # summary = 750 / 12.5 = 60.0
    assert abs(summary - 60.0) < 0.01


def test_negative_tb_values(engine):
    points = _make_lifetime([-3.0] * 12)
    assert abs(engine._summary_score(points) - (-3.0)) < 0.01


def test_mixed_positive_negative(engine):
    """Verify weighted average handles mixed values."""
    # All prime = +10, all non-prime = -10
    tb_values = [-10, -10, 10, 10, 10, 10, 10, -10, -10, -10, -10, -10]
    summary = engine._summary_score(_make_lifetime(tb_values))

    # Manual: prime contribution = 5 * 1.5 * 10 = 75
    # non-prime: (2*0.5 + 3*1.0 + 2*0.5) * (-10) = 5 * (-10) = -50
    # total_weight = 12.5
    # summary = (75 - 50) / 12.5 = 2.0
    assert abs(summary - 2.0) < 0.01
