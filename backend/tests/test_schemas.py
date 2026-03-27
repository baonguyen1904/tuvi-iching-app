from app.models.schemas import CungDetail, CungInfo, LaSoTuVi, LaSoTuViInput


def test_cung_detail_basic():
    cung = CungDetail(ten="Mệnh", sao=["Tử Vi (B)", "Lộc Tồn"])
    assert cung.ten == "Mệnh"
    assert len(cung.sao) == 2
    assert cung.thang is None


def test_cung_detail_with_month():
    cung = CungDetail(ten="Tài Bạch", sao=["Liêm Trinh (Đ)"], thang="Th.2")
    assert cung.thang == "Th.2"


def test_cung_info():
    cung = CungDetail(ten="Mệnh", sao=["Tử Vi (B)"])
    info = CungInfo(
        cung_chung=[cung],
        cung_10yrs=[],
        cung_12months=[],
    )
    assert len(info.cung_chung) == 1
    assert info.cung_10yrs == []


def test_la_so_tu_vi_minimal():
    la_so = LaSoTuVi(
        ngay_sinh="1997-10-11",
        gio_sinh="12h00",
        gender="Nam",
    )
    assert la_so.menh is None
    assert la_so.cung is None
    assert la_so.am_duong is None


def test_la_so_tu_vi_full():
    cung = CungDetail(ten="Mệnh", sao=["Vũ Khúc (H)"])
    info = CungInfo(cung_chung=[cung], cung_10yrs=[], cung_12months=[])
    la_so = LaSoTuVi(
        ngay_sinh="1997-10-11",
        gio_sinh="12h00",
        gender="Nam",
        am_duong="Âm Nam",
        menh="Giáng Hạ Thủy",
        cuc="Kim Tứ Cục",
        than_cu="Phu thê",
        menh_chu="Cự môn",
        than_chu="Thiên tướng",
        cung=info,
    )
    assert la_so.am_duong == "Âm Nam"
    assert la_so.cung.cung_chung[0].ten == "Mệnh"


def test_la_so_tu_vi_input():
    inp = LaSoTuViInput(
        ngay_sinh="11/10/1997",
        gio_sinh="12h00",
        gender="Nam",
        nam_xem=2026,
    )
    assert inp.nam_xem == 2026
    assert inp.full_name is None


def test_la_so_tu_vi_json_roundtrip():
    cung = CungDetail(ten="Mệnh", sao=["Tử Vi (B)", "Lộc Tồn"])
    info = CungInfo(cung_chung=[cung], cung_10yrs=[], cung_12months=[])
    la_so = LaSoTuVi(
        ngay_sinh="1997-10-11",
        gio_sinh="12h00",
        gender="Nam",
        am_duong="Âm Nam",
        cung=info,
    )
    data = la_so.model_dump()
    restored = LaSoTuVi(**data)
    assert restored.cung.cung_chung[0].sao == ["Tử Vi (B)", "Lộc Tồn"]
