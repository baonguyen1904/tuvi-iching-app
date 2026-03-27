"""Tests for AI output validation."""
from app.services.ai_engine import validate_output


def test_validate_output_clean():
    text = "## Tổng quan Sự Nghiệp\nLuận giải chi tiết dài hơn hai trăm ký tự để pass validation. " * 3 + "\n\n---\n*Đây là luận giải tham khảo dựa trên Tử Vi Đẩu Số. Mọi quyết định cuối cùng là của bạn.*"
    warnings = validate_output(text, "su_nghiep")
    assert warnings == []


def test_validate_output_forbidden_phrase_se_gap_hoa():
    text = "Bạn sẽ gặp họa trong năm 2027. " * 10 + "\n---\n*Tham khảo.*"
    warnings = validate_output(text, "su_nghiep")
    assert any("sẽ gặp họa" in w for w in warnings)


def test_validate_output_forbidden_phrase_chac_chan_se():
    text = "Bạn chắc chắn sẽ thành công lớn trong năm tới. " * 10 + "\n---\n*Tham khảo.*"
    warnings = validate_output(text, "su_nghiep")
    assert any("chắc chắn sẽ" in w for w in warnings)


def test_validate_output_forbidden_phrase_tuyet_doi():
    text = "Điều này tuyệt đối đúng với mọi trường hợp. " * 10 + "\n---\n*Tham khảo.*"
    warnings = validate_output(text, "su_nghiep")
    assert any("tuyệt đối" in w for w in warnings)


def test_validate_output_no_disclaimer():
    text = "## Tổng quan Sự Nghiệp\n" + "Luận giải xong. " * 20
    warnings = validate_output(text, "su_nghiep")
    assert any("disclaimer" in w.lower() or "tham khảo" in w.lower() for w in warnings)


def test_validate_output_too_short():
    text = "OK."
    warnings = validate_output(text, "su_nghiep")
    assert any("SHORT" in w for w in warnings)


def test_validate_output_too_long():
    text = "x" * 5001 + "\n---\n*Tham khảo.*"
    warnings = validate_output(text, "su_nghiep")
    assert any("LONG" in w for w in warnings)


def test_validate_output_no_headings():
    text = "Luận giải không có heading nào cả. " * 15 + "\n---\n*Tham khảo.*"
    warnings = validate_output(text, "su_nghiep")
    assert any("heading" in w.lower() or "##" in w for w in warnings)
