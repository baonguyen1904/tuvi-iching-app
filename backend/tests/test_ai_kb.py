import pytest
from app.services.ai_engine import KnowledgeBase, load_kb, KBLoadError


def test_load_kb_all_core_files():
    kb = load_kb("knowledge_base")
    assert "scoring_rules" in kb.core
    assert "alert_interpretation" in kb.core
    assert "tone_guidelines" in kb.core
    assert len(kb.core) == 3


def test_load_kb_all_dimensions():
    kb = load_kb("knowledge_base")
    expected = ["su_nghiep", "tien_bac", "hon_nhan", "suc_khoe", "dat_dai", "hoc_tap", "con_cai"]
    for dim in expected:
        assert dim in kb.dimensions, f"Missing dimension: {dim}"
    assert len(kb.dimensions) == 7


def test_load_kb_stars():
    kb = load_kb("knowledge_base")
    assert "chinh_tinh" in kb.stars
    assert "phu_tinh" in kb.stars


def test_load_kb_examples():
    kb = load_kb("knowledge_base")
    assert "sample_su_nghiep" in kb.examples


def test_load_kb_nonempty_content():
    kb = load_kb("knowledge_base")
    for key, content in kb.core.items():
        assert len(content) > 50, f"Core KB '{key}' too short"
    for key, content in kb.dimensions.items():
        assert len(content) > 100, f"Dimension KB '{key}' too short"


def test_load_kb_missing_dir_raises():
    with pytest.raises(KBLoadError):
        load_kb("/nonexistent/path")
