from app.models.schemas import (
    UserProfile,
    LasoMetadata,
    InterpretationResult,
)
from datetime import date


def test_user_profile_with_name():
    user = UserProfile(
        name="Nguyễn Văn A",
        birth_date=date(1994, 7, 19),
        birth_hour="dan",
        birth_hour_label="Giờ Dần (03:00-05:00)",
        gender="male",
        gender_label="Nam",
        current_age=31,
        nam_xem=2026,
    )
    assert user.name == "Nguyễn Văn A"
    assert user.display_name == "Nguyễn Văn A"


def test_user_profile_without_name():
    user = UserProfile(
        name=None,
        birth_date=date(1994, 7, 19),
        birth_hour="dan",
        birth_hour_label="Giờ Dần (03:00-05:00)",
        gender="male",
        gender_label="Nam",
        current_age=31,
        nam_xem=2026,
    )
    assert user.display_name == "Bạn"


def test_interpretation_result_all_success():
    result = InterpretationResult(
        overview="Tổng quan...",
        dimensions={"su_nghiep": "## Tổng quan...", "tien_bac": "## Tiền bạc..."},
        errors={},
        token_usage={"su_nghiep": (5000, 1200)},
    )
    assert result.has_errors is False
    assert result.completed_count == 2


def test_interpretation_result_partial_failure():
    result = InterpretationResult(
        overview="Tổng quan...",
        dimensions={"su_nghiep": "## Tổng quan..."},
        errors={"tien_bac": "RateLimitError"},
        token_usage={},
    )
    assert result.has_errors is True
    assert result.completed_count == 1


def test_laso_metadata():
    meta = LasoMetadata(
        nam="Giáp Tuất",
        menh="Mộc",
        cuc="Thủy Nhị Cục",
        am_duong="Dương Nam",
        cung_menh="Mệnh",
    )
    assert meta.nam == "Giáp Tuất"
    assert meta.menh == "Mộc"
