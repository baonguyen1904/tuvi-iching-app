"""Tests for AIEngine API calling with mocked Claude API."""
import json
from datetime import date
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import anthropic
import pytest

from app.models.schemas import (
    UserProfile, LasoMetadata, ScorePoint, Alert,
    DimensionScores, ScoringResult,
)
from app.services.ai_engine import AIEngine


# --- Fixtures ---

def _make_user() -> UserProfile:
    return UserProfile(
        name="Nguyễn Văn A",
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


def _mock_response(text: str = "## Tổng quan\nMock luận giải.\n\n---\n*Tham khảo.*"):
    """Create a mock Claude API response."""
    msg = MagicMock()
    msg.content = [MagicMock(text=text)]
    msg.usage = MagicMock()
    msg.usage.input_tokens = 5000
    msg.usage.output_tokens = 1200
    return msg


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


# --- generate_dimension tests ---


@pytest.mark.asyncio
async def test_generate_dimension_returns_text(engine, user, metadata, scoring, laso):
    """Mock Claude API, verify text returned."""
    mock_resp = _mock_response("## Tổng quan Sự Nghiệp\nLuận giải chi tiết...")

    with patch.object(
        engine._client.messages, "create",
        new_callable=AsyncMock, return_value=mock_resp,
    ):
        result = await engine.generate_dimension(
            "su_nghiep", user, metadata, laso, scoring.dimensions["su_nghiep"]
        )

    assert "Tổng quan" in result
    assert isinstance(result, str)


@pytest.mark.asyncio
async def test_generate_dimension_retries_on_rate_limit(engine, user, metadata, scoring, laso):
    """Verify retry on rate limit errors."""
    error_resp = MagicMock()
    error_resp.status_code = 429
    error_resp.headers = {}
    error = anthropic.RateLimitError(
        message="rate limited",
        response=error_resp,
        body={"error": {"message": "rate limited"}},
    )
    success = _mock_response("OK")

    with patch.object(
        engine._client.messages, "create",
        new_callable=AsyncMock,
        side_effect=[error, success],
    ):
        result = await engine.generate_dimension(
            "su_nghiep", user, metadata, laso, scoring.dimensions["su_nghiep"]
        )

    assert result == "OK"


@pytest.mark.asyncio
async def test_generate_dimension_raises_after_max_retries(engine, user, metadata, scoring, laso):
    """Verify exception after exhausting retries."""
    error_resp = MagicMock()
    error_resp.status_code = 429
    error_resp.headers = {}
    error = anthropic.RateLimitError(
        message="rate limited",
        response=error_resp,
        body={"error": {"message": "rate limited"}},
    )

    with patch.object(
        engine._client.messages, "create",
        new_callable=AsyncMock,
        side_effect=[error, error, error],
    ):
        with pytest.raises(anthropic.RateLimitError):
            await engine.generate_dimension(
                "su_nghiep", user, metadata, laso, scoring.dimensions["su_nghiep"]
            )


# --- generate_overview tests ---


@pytest.mark.asyncio
async def test_generate_overview_returns_text(engine, user, metadata, scoring):
    """Mock Claude API for overview generation."""
    mock_resp = _mock_response("Tổng quan vận mệnh của bạn...")

    with patch.object(
        engine._client.messages, "create",
        new_callable=AsyncMock, return_value=mock_resp,
    ):
        result = await engine.generate_overview(user, metadata, scoring)

    assert "Tổng quan" in result
    assert isinstance(result, str)
