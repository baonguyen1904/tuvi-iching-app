"""Integration tests for the full AI pipeline with mocked Claude API."""
import json
from datetime import date
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models.schemas import (
    UserProfile, LasoMetadata, ScorePoint, Alert,
    DimensionScores, ScoringResult,
)
from app.services.ai_engine import AIEngine


# --- Helpers ---

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


def _load_fixture(name: str):
    fixture = Path(__file__).parent / "fixtures" / name
    return json.loads(fixture.read_text())


def _load_scoring() -> ScoringResult:
    data = _load_fixture("sample_scoring.json")
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


# --- Integration Tests ---


@pytest.mark.asyncio
async def test_full_pipeline_with_mocked_api():
    """
    Load real KB files -> build prompts -> mock API returns canned response ->
    verify InterpretationResult structure.
    """
    engine = AIEngine(kb_dir="knowledge_base", api_key="test")

    scoring = _load_scoring()
    user = _make_user()
    metadata = _make_metadata()
    laso = _load_fixture("sample_laso.json")

    # Mock API to return dimension-specific canned text
    async def mock_create(**kwargs):
        msg = MagicMock()
        msg.content = [MagicMock(
            text="## Tổng quan\nMock luận giải chi tiết đủ dài để pass validation check. "
                 "Đây là nội dung được tạo tự động để test. " * 5
                 + "\n\n---\n*Đây là luận giải tham khảo dựa trên Tử Vi Đẩu Số. "
                 "Mọi quyết định cuối cùng là của bạn.*"
        )]
        msg.usage = MagicMock()
        msg.usage.input_tokens = 5000
        msg.usage.output_tokens = 1000
        return msg

    with patch.object(engine._client.messages, "create", side_effect=mock_create):
        result = await engine.generate_all(user, metadata, laso, scoring)

    assert len(result.dimensions) == 7
    assert result.overview is not None
    assert len(result.overview) > 0
    assert not result.has_errors
    for dim, text in result.dimensions.items():
        assert len(text) > 10, f"Dimension {dim} text too short"


@pytest.mark.asyncio
async def test_full_pipeline_overview_fails_gracefully():
    """Overview fails but dimensions succeed."""
    engine = AIEngine(kb_dir="knowledge_base", api_key="test")

    scoring = _load_scoring()
    user = _make_user()
    metadata = _make_metadata()
    laso = _load_fixture("sample_laso.json")

    call_count = 0

    async def mock_create(**kwargs):
        nonlocal call_count
        call_count += 1
        # First call is overview — fail it
        if call_count == 1:
            raise RuntimeError("Overview API failure")
        msg = MagicMock()
        msg.content = [MagicMock(text="## Tổng quan\nMock text.\n\n---\n*Tham khảo.*")]
        msg.usage = MagicMock()
        msg.usage.input_tokens = 5000
        msg.usage.output_tokens = 1000
        return msg

    with patch.object(engine._client.messages, "create", side_effect=mock_create):
        result = await engine.generate_all(user, metadata, laso, scoring)

    assert len(result.dimensions) == 7
    assert result.has_errors
    assert "overview" in result.errors


def test_prompt_token_count_within_budget():
    """Verify prompts don't exceed expected token budget."""
    engine = AIEngine(kb_dir="knowledge_base", api_key="test")

    scoring = _load_scoring()
    user = _make_user()
    metadata = _make_metadata()
    laso = _load_fixture("sample_laso.json")

    system, user_msg = engine._build_dimension_prompt(
        "su_nghiep", user, metadata, laso, scoring.dimensions["su_nghiep"]
    )

    # Rough estimate: Vietnamese uses ~3 chars/token
    total_chars = len(system) + len(user_msg)
    estimated_tokens = total_chars / 3
    assert estimated_tokens < 10000, f"Prompt too large: ~{estimated_tokens:.0f} tokens"


def test_all_dimensions_produce_prompts():
    """Verify every dimension produces valid prompts."""
    engine = AIEngine(kb_dir="knowledge_base", api_key="test")

    scoring = _load_scoring()
    user = _make_user()
    metadata = _make_metadata()
    laso = _load_fixture("sample_laso.json")

    dims = ["su_nghiep", "tien_bac", "hon_nhan", "suc_khoe", "dat_dai", "hoc_tap", "con_cai"]
    for dim in dims:
        system, user_msg = engine._build_dimension_prompt(
            dim, user, metadata, laso, scoring.dimensions[dim]
        )
        assert len(system) > 500, f"System prompt for {dim} too short"
        assert len(user_msg) > 200, f"User prompt for {dim} too short"
