COHOC_FORM_URL = "http://tuvi.cohoc.net/lay-la-so-tu-vi-ngay-duong-lich.html"
TUVIVN_FORM_URL = "https://tuvi.vn/lap-la-so-tu-vi"

# Hour → [start_hour, end_hour] mapping for cohoc.net form
GIO_SINH = {
    1: [23, 1],
    2: [1, 3],
    3: [3, 5],
    4: [5, 7],
    5: [7, 9],
    6: [9, 11],
    7: [11, 13],
    8: [13, 15],
    9: [15, 17],
    10: [17, 19],
    11: [19, 21],
    12: [21, 23],
}

# Lunar year names by Gregorian year
LUNA_YEARS = {
    2022: "Dần",
    2023: "Mão",
    2024: "Thìn",
    2025: "Tị",
    2026: "Ngọ",
    2027: "Mùi",
    2028: "Thân",
    2029: "Dậu",
    2030: "Tuất",
    2031: "Hợi",
    2032: "Tí",
    2033: "Sửu",
    2034: "Dần",
    2035: "Mão",
    2036: "Thìn",
    2037: "Tị",
    2038: "Ngọ",
    2039: "Mùi",
    2040: "Thân",
    2041: "Dậu",
    2042: "Tuất",
    2043: "Hợi",
}

# Cung reorder arrays (position indices in the HTML grid)
# Dương Nam / Âm Nữ
MAIN_ORDER = [0, 1, 2, 3, 5, 7, 11, 10, 9, 8, 6, 4]
# Âm Nam / Dương Nữ
REVERSED_ORDER = [0, 4, 6, 8, 9, 10, 11, 7, 5, 3, 2, 1]
