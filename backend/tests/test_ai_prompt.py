"""Tests for prompt building (dimension + overview)."""
import json
from datetime import date
from pathlib import Path

import pytest

from app.models.schemas import (
    UserProfile, LasoMetadata, ScorePoint, Alert,
    DimensionScores, ScoringResult,
)
from app.services.ai_engine import AIEngine


# --- Fixtures ---

def _make_user(name: str | None = "Nguyễn Văn A") -> UserProfile:
    return UserProfile(
        name=name,
        birth_date=date(1994, 7, 19),
        birth_hour="dan",
        birth_hour_label="Giờ Dần (03:00-05:00)",
        gender="male",
        gender_label="Nam",
        current_age=31,
        nam_xem=2026,
    )


def _make_metadata() -> LasoMetadata:
    return LasoMetadata(
        nam="Giáp Tuất",
        menh="Mộc",
        cuc="Thủy Nhị Cục",
        am_duong="Dương Nam",
        cung_menh="Mệnh",
    )


def _load_scoring() -> ScoringResult:
    fixture = Path(__file__).parent / "fixtures" / "sample_scoring.json"
    data = json.loads(fixture.read_text())
    dims = {}
    for key, d in data["dimensions"].items():
        dims[key] = DimensionScores(
            dimension=d["dimension"],
            label=d["label"],
            lifetime=[ScorePoint(**p) for p in d["lifetime"]],
            decade=[ScorePoint(**p) for p in d["decade"]],
            monthly=[ScorePoint(**p) for p in d["monthly"]],
            alerts=[Alert(**a) for a in d["alerts"]],
            summary_score=d["summary_score"],
        )
    all_alerts = [Alert(**a) for a in data["all_alerts"]]
    return ScoringResult(dimensions=dims, all_alerts=all_alerts)


def _load_laso() -> dict:
    fixture = Path(__file__).parent / "fixtures" / "sample_laso.json"
    return json.loads(fixture.read_text())


@pytest.fixture
def engine():
    return AIEngine(kb_dir="knowledge_base", api_key="test-key")


@pytest.fixture
def user():
    return _make_user()


@pytest.fixture
def metadata():
    return _make_metadata()


@pytest.fixture
def scoring():
    return _load_scoring()


@pytest.fixture
def laso():
    return _load_laso()


# --- Dimension Prompt Tests ---

def test_dimension_prompt_has_system_and_user(engine, user, metadata, scoring, laso):
    system, user_msg = engine._build_dimension_prompt(
        "su_nghiep", user, metadata, laso, scoring.dimensions["su_nghiep"]
    )
    assert isinstance(system, str)
    assert isinstance(user_msg, str)
    assert len(system) > 500
    assert len(user_msg) > 200


def test_dimension_prompt_contains_role(engine, user, metadata, scoring, laso):
    system, _ = engine._build_dimension_prompt(
        "su_nghiep", user, metadata, laso, scoring.dimensions["su_nghiep"]
    )
    assert "tư vấn viên luận giải tử vi" in system


def test_dimension_prompt_contains_rules(engine, user, metadata, scoring, laso):
    system, _ = engine._build_dimension_prompt(
        "su_nghiep", user, metadata, laso, scoring.dimensions["su_nghiep"]
    )
    assert "KHÔNG bịa đặt" in system
    assert "cần thận trọng" in system


def test_dimension_prompt_contains_core_kb(engine, user, metadata, scoring, laso):
    system, _ = engine._build_dimension_prompt(
        "su_nghiep", user, metadata, laso, scoring.dimensions["su_nghiep"]
    )
    assert "Dương" in system
    assert "🔺" in system or "🔻" in system


def test_dimension_prompt_contains_dimension_kb(engine, user, metadata, scoring, laso):
    system, _ = engine._build_dimension_prompt(
        "su_nghiep", user, metadata, laso, scoring.dimensions["su_nghiep"]
    )
    assert "Quan Lộc" in system


def test_dimension_prompt_user_contains_scores(engine, user, metadata, scoring, laso):
    _, user_msg = engine._build_dimension_prompt(
        "su_nghiep", user, metadata, laso, scoring.dimensions["su_nghiep"]
    )
    assert "| Giai đoạn |" in user_msg
    assert "| Năm |" in user_msg
    assert "| Tháng |" in user_msg


def test_dimension_prompt_user_contains_alerts(engine, user, metadata, scoring, laso):
    _, user_msg = engine._build_dimension_prompt(
        "su_nghiep", user, metadata, laso, scoring.dimensions["su_nghiep"]
    )
    assert "🔺" in user_msg or "🔻" in user_msg or "Không có cảnh báo" in user_msg


def test_dimension_prompt_user_contains_format(engine, user, metadata, scoring, laso):
    _, user_msg = engine._build_dimension_prompt(
        "su_nghiep", user, metadata, laso, scoring.dimensions["su_nghiep"]
    )
    assert "## Tổng quan" in user_msg
    assert "## Lời khuyên" in user_msg
    assert "tham khảo" in user_msg.lower()


def test_dimension_prompt_user_name_none_uses_ban(engine, metadata, scoring, laso):
    user_none = _make_user(name=None)
    _, user_msg = engine._build_dimension_prompt(
        "su_nghiep", user_none, metadata, laso, scoring.dimensions["su_nghiep"]
    )
    assert "Bạn" in user_msg


def test_dimension_prompt_different_dimensions_have_different_kb(engine, user, metadata, scoring, laso):
    sys_sn, _ = engine._build_dimension_prompt(
        "su_nghiep", user, metadata, laso, scoring.dimensions["su_nghiep"]
    )
    sys_tb, _ = engine._build_dimension_prompt(
        "tien_bac", user, metadata, laso, scoring.dimensions["tien_bac"]
    )
    assert sys_sn != sys_tb
