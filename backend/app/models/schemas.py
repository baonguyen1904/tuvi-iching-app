from typing import Optional

from pydantic import BaseModel


class CungDetail(BaseModel):
    ten: str
    sao: list[str]
    thang: Optional[str] = None


class CungInfo(BaseModel):
    cung_chung: list[CungDetail]
    cung_10yrs: list[CungDetail]
    cung_12months: list[CungDetail]


class LaSoTuVi(BaseModel):
    ngay_sinh: str
    gio_sinh: str
    gender: str
    nam_am_lich: Optional[str] = None
    menh: Optional[str] = None
    cuc: Optional[str] = None
    than_cu: Optional[str] = None
    menh_chu: Optional[str] = None
    than_chu: Optional[str] = None
    am_duong: Optional[str] = None
    cung: Optional[CungInfo] = None


class LaSoTuViInput(BaseModel):
    ngay_sinh: str
    gio_sinh: str
    gender: str
    full_name: Optional[str] = None
    nam_xem: Optional[int] = None
    noi_sinh: Optional[str] = None
