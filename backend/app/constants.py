"""Scoring engine constants — house weights, age weights, dimension config."""

DIMENSIONS: list[str] = [
    "van_menh",
    "su_nghiep",
    "tien_bac",
    "hon_nhan",
    "suc_khoe",
    "dat_dai",
    "hoc_tap",
    "con_cai",
]

# House weighting anchor config per dimension.
# Each entry: (cung_name, weight). Weights sum to 1.0.
# "thân" is a dynamic reference resolved via laso.than_cu at runtime.
HOUSE_WEIGHTS: dict[str, list[tuple[str, float]]] = {
    "van_menh": [("mệnh", 0.4), ("thân", 0.2), ("quan lộc", 0.2), ("tài bạch", 0.2)],
    "su_nghiep": [("quan lộc", 0.4), ("mệnh", 0.2), ("tài bạch", 0.2), ("thiên di", 0.2)],
    "tien_bac": [("tài bạch", 0.4), ("mệnh", 0.2), ("quan lộc", 0.2), ("điền trạch", 0.2)],
    "hon_nhan": [("phu thê", 0.4), ("mệnh", 0.2), ("phúc đức", 0.2), ("nô bộc", 0.2)],
    "suc_khoe": [("tật ách", 0.6), ("phúc đức", 0.4)],
    "dat_dai": [("tật ách", 0.6), ("phúc đức", 0.4)],
    "hoc_tap": [("mệnh", 0.5), ("quan lộc", 0.2), ("thiên di", 0.3)],
    "con_cai": [("tử tức", 0.5), ("điền trạch", 0.1), ("phúc đức", 0.4)],
}

# 3-tier age weights for summary_score calculation.
# Prime years (20-60) weighted higher, childhood/old age weighted lower.
SUMMARY_AGE_WEIGHTS: dict[int, float] = {
    0: 0.5,
    10: 0.5,
    20: 1.5,
    30: 1.5,
    40: 1.5,
    50: 1.5,
    60: 1.5,
    70: 1.0,
    80: 1.0,
    90: 1.0,
    100: 0.5,
    110: 0.5,
}

DIMENSION_LABELS: dict[str, str] = {
    "van_menh": "Vận Mệnh",
    "su_nghiep": "Sự Nghiệp",
    "tien_bac": "Tiền Bạc",
    "hon_nhan": "Hôn Nhân",
    "suc_khoe": "Sức Khỏe",
    "dat_dai": "Đất Đai",
    "hoc_tap": "Học Tập",
    "con_cai": "Con Cái",
}
