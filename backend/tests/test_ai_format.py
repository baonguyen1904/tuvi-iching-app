from app.services.ai_engine import format_scores_table, format_alerts
from app.models.schemas import ScorePoint, Alert


def test_format_lifetime_table():
    points = [
        ScorePoint(period="0-10", duong=15.20, am=-8.30, tb=6.90),
        ScorePoint(period="10-20", duong=18.40, am=-5.10, tb=13.30),
    ]
    table = format_scores_table(points)
    assert "| Giai đoạn | Dương | Âm | TB |" in table
    assert "| 0-10 | 15.20 | -8.30 | 6.90 |" in table
    assert "| 10-20 | 18.40 | -5.10 | 13.30 |" in table


def test_format_decade_table():
    points = [ScorePoint(period="2026", duong=12.50, am=-6.20, tb=6.30)]
    table = format_scores_table(points, header="Năm")
    assert "| Năm | Dương | Âm | TB |" in table


def test_format_monthly_table():
    points = [ScorePoint(period="Th.1/2026", duong=10.00, am=-4.50, tb=5.50)]
    table = format_scores_table(points, header="Tháng")
    assert "| Tháng | Dương | Âm | TB |" in table


def test_format_alerts_positive():
    alerts = [
        Alert(type="positive", dimension="su_nghiep", period="2027",
              tag="có bước thăng tiến", level=50, star_name="hoa-cai"),
    ]
    text = format_alerts(alerts)
    assert "🔺" in text
    assert "2027" in text
    assert "có bước thăng tiến" in text


def test_format_alerts_negative():
    alerts = [
        Alert(type="negative", dimension="su_nghiep", period="2029",
              tag="cẩn thận kiện cáo", level=30, star_name="da-la"),
    ]
    text = format_alerts(alerts)
    assert "🔻" in text


def test_format_alerts_empty():
    text = format_alerts([])
    assert "Không có cảnh báo đặc biệt" in text


def test_format_alerts_sorted_by_level():
    alerts = [
        Alert(type="negative", dimension="su_nghiep", period="2029",
              tag="cẩn thận", level=30, star_name="x"),
        Alert(type="positive", dimension="su_nghiep", period="2027",
              tag="thăng tiến", level=50, star_name="y"),
    ]
    text = format_alerts(alerts)
    # Level 50 should appear before level 30
    pos_50 = text.index("thăng tiến")
    pos_30 = text.index("cẩn thận")
    assert pos_50 < pos_30
