from app.constants import (
    HOUSE_WEIGHTS,
    SUMMARY_AGE_WEIGHTS,
    DIMENSION_LABELS,
    DIMENSIONS,
)


def test_dimensions_count():
    assert len(DIMENSIONS) == 8


def test_dimensions_order():
    assert DIMENSIONS[0] == "van_menh"
    assert DIMENSIONS[-1] == "con_cai"


def test_house_weights_cover_all_dimensions():
    for dim in DIMENSIONS:
        assert dim in HOUSE_WEIGHTS, f"Missing house weights for {dim}"


def test_house_weights_sum_to_one():
    for dim, weights in HOUSE_WEIGHTS.items():
        total = sum(w for _, w in weights)
        assert abs(total - 1.0) < 0.01, f"{dim} weights sum to {total}, expected 1.0"


def test_summary_age_weights_cover_12_ages():
    ages = sorted(SUMMARY_AGE_WEIGHTS.keys())
    assert ages == list(range(0, 120, 10))


def test_dimension_labels_cover_all():
    for dim in DIMENSIONS:
        assert dim in DIMENSION_LABELS
        assert isinstance(DIMENSION_LABELS[dim], str)
        assert len(DIMENSION_LABELS[dim]) > 0
