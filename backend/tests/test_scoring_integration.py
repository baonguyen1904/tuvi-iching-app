import json
from pathlib import Path
from dataclasses import dataclass

import pytest
from app.services.scoring import ScoringEngine
from app.constants import DIMENSIONS, DIMENSION_LABELS

XLSX_PATH = str(Path(__file__).resolve().parents[2] / "data" / "laso_points.xlsx")
FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "sample_laso.json"


@dataclass
class FixtureStar:
    name: str
    raw_name: str
    variant: str | None
    slug: str


@dataclass
class FixtureCung:
    name: str
    stars: list[FixtureStar]


@dataclass
class FixtureMonthlyCung:
    name: str
    month: int
    month_label: str
    stars: list[FixtureStar]


@dataclass
class FixtureLasoData:
    nam: str
    menh: str
    cuc: str
    than_cu: str
    menh_chu: str
    than_chu: str
    am_duong: str
    cung: list[FixtureCung]
    cung_10yrs: list[FixtureCung]
    cung_12months: list[FixtureMonthlyCung]


def _load_fixture() -> FixtureLasoData:
    data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    return FixtureLasoData(
        nam=data["nam"],
        menh=data["menh"],
        cuc=data["cuc"],
        than_cu=data["than_cu"],
        menh_chu=data["menh_chu"],
        than_chu=data["than_chu"],
        am_duong=data["am_duong"],
        cung=[
            FixtureCung(
                name=c["name"],
                stars=[FixtureStar(**s) for s in c["stars"]],
            )
            for c in data["cung"]
        ],
        cung_10yrs=[
            FixtureCung(
                name=c["name"],
                stars=[FixtureStar(**s) for s in c["stars"]],
            )
            for c in data["cung_10yrs"]
        ],
        cung_12months=[
            FixtureMonthlyCung(
                name=c["name"],
                month=c["month"],
                month_label=c["month_label"],
                stars=[FixtureStar(**s) for s in c["stars"]],
            )
            for c in data["cung_12months"]
        ],
    )


@pytest.fixture(scope="module")
def engine():
    return ScoringEngine(xlsx_path=XLSX_PATH)


@pytest.fixture(scope="module")
def laso():
    return _load_fixture()


@pytest.fixture(scope="module")
def result(engine, laso):
    return engine.score(laso)


def test_result_has_8_dimensions(result):
    assert len(result.dimensions) == 8
    for dim in DIMENSIONS:
        assert dim in result.dimensions


def test_dimension_labels_correct(result):
    for dim_key, dim_scores in result.dimensions.items():
        assert dim_scores.label == DIMENSION_LABELS[dim_key]


def test_lifetime_has_12_points(result):
    for dim_key, dim_scores in result.dimensions.items():
        assert len(dim_scores.lifetime) == 12, f"{dim_key} lifetime has {len(dim_scores.lifetime)} points"


def test_decade_has_10_points(result):
    for dim_key, dim_scores in result.dimensions.items():
        assert len(dim_scores.decade) == 10, f"{dim_key} decade has {len(dim_scores.decade)} points"


def test_monthly_has_13_points(result):
    for dim_key, dim_scores in result.dimensions.items():
        assert len(dim_scores.monthly) == 13, f"{dim_key} monthly has {len(dim_scores.monthly)} points"


def test_monthly_first_two_periods_same(result):
    """First month is prepended -> first two periods should match."""
    for dim_key, dim_scores in result.dimensions.items():
        assert dim_scores.monthly[0].period == dim_scores.monthly[1].period, (
            f"{dim_key}: monthly[0].period={dim_scores.monthly[0].period} "
            f"!= monthly[1].period={dim_scores.monthly[1].period}"
        )


def test_tb_equals_duong_plus_am(result):
    """tb must always equal duong + am (algebraic sum)."""
    for dim_key, dim_scores in result.dimensions.items():
        for chart_name in ("lifetime", "decade", "monthly"):
            for point in getattr(dim_scores, chart_name):
                expected_tb = round(point.duong + point.am, 2)
                assert abs(point.tb - expected_tb) < 0.02, (
                    f"{dim_key}.{chart_name} period {point.period}: "
                    f"tb={point.tb} != duong({point.duong}) + am({point.am}) = {expected_tb}"
                )


def test_van_menh_has_no_alerts(result):
    assert len(result.dimensions["van_menh"].alerts) == 0


def test_all_alerts_flattened(result):
    total_from_dims = sum(len(d.alerts) for d in result.dimensions.values())
    assert len(result.all_alerts) == total_from_dims


def test_all_alerts_sorted_by_level_desc(result):
    for i in range(1, len(result.all_alerts)):
        assert result.all_alerts[i - 1].level >= result.all_alerts[i].level


def test_summary_score_is_number(result):
    for dim_key, dim_scores in result.dimensions.items():
        assert isinstance(dim_scores.summary_score, float)


def test_lifetime_periods_are_age_ranges(result):
    expected = [f"{a}-{a+10}" for a in range(0, 120, 10)]
    for dim_key, dim_scores in result.dimensions.items():
        actual = [p.period for p in dim_scores.lifetime]
        assert actual == expected, f"{dim_key} lifetime periods: {actual}"


def test_decade_periods_are_years(result):
    dim_scores = result.dimensions["su_nghiep"]
    periods = [p.period for p in dim_scores.decade]
    # Should be consecutive years
    for p in periods:
        assert p.isdigit(), f"Decade period '{p}' is not a year"
    years = [int(p) for p in periods]
    assert years == list(range(years[0], years[0] + 10))


def test_scoring_error_on_insufficient_cungs(engine):
    """Raise ScoringError if fewer than 12 lifetime cungs."""
    from app.services.scoring import ScoringError

    bad_laso = FixtureLasoData(
        nam="Test", menh="Moc", cuc="Test", than_cu="Menh",
        menh_chu="Test", than_chu="Test", am_duong="Test",
        cung=[FixtureCung(name="Menh", stars=[])],  # only 1
        cung_10yrs=[FixtureCung(name=f"C{i}", stars=[]) for i in range(12)],
        cung_12months=[
            FixtureMonthlyCung(name=f"C{i}", month=i+1, month_label=f"Th.{i+1}", stars=[])
            for i in range(12)
        ],
    )
    with pytest.raises(ScoringError, match="12 lifetime"):
        engine.score(bad_laso)


def test_scoring_error_on_insufficient_months(engine):
    """Raise ScoringError if fewer than 12 monthly cungs."""
    from app.services.scoring import ScoringError

    bad_laso = FixtureLasoData(
        nam="Test", menh="Moc", cuc="Test", than_cu="Menh",
        menh_chu="Test", than_chu="Test", am_duong="Test",
        cung=[FixtureCung(name=f"C{i}", stars=[]) for i in range(12)],
        cung_10yrs=[FixtureCung(name=f"C{i}", stars=[]) for i in range(12)],
        cung_12months=[
            FixtureMonthlyCung(name="C0", month=1, month_label="Th.1", stars=[])
        ],  # only 1
    )
    with pytest.raises(ScoringError, match="12 monthly"):
        engine.score(bad_laso)


def test_scoring_with_empty_stars_produces_zero_scores(engine):
    """All cungs with no stars -> all scores should be 0."""
    empty_laso = FixtureLasoData(
        nam="Test", menh="Moc", cuc="Test", than_cu="Menh",
        menh_chu="Test", than_chu="Test", am_duong="Test",
        cung=[FixtureCung(name=f"C{i}", stars=[]) for i in range(12)],
        cung_10yrs=[FixtureCung(name=f"C{i}", stars=[]) for i in range(12)],
        cung_12months=[
            FixtureMonthlyCung(name=f"C{i}", month=i+1, month_label=f"Th.{i+1}", stars=[])
            for i in range(12)
        ],
    )
    result = engine.score(empty_laso)

    for dim_key, dim_scores in result.dimensions.items():
        for point in dim_scores.lifetime:
            assert point.duong == 0.0
            assert point.am == 0.0
            assert point.tb == 0.0


def test_scoring_performance(engine, laso):
    """Scoring must complete in < 200ms."""
    import time
    start = time.perf_counter()
    for _ in range(10):
        engine.score(laso)
    elapsed = (time.perf_counter() - start) / 10
    assert elapsed < 0.2, f"Scoring took {elapsed:.3f}s, expected < 0.2s"
