from dataclasses import dataclass, field
from datetime import date
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


# --- Scoring output types ---


@dataclass
class StarRow:
    """One row from laso_points.xlsx, indexed by slug."""
    slug: str
    name: str
    point: int
    weights: dict[str, float] = field(default_factory=dict)
    alert_tags: dict[str, dict[int, str | None]] = field(default_factory=dict)
    pct_fvg: dict[int, str | None] = field(default_factory=dict)


@dataclass
class ScorePoint:
    """One data point on a chart line."""
    period: str
    duong: float
    am: float
    tb: float


@dataclass
class Alert:
    """A detected score change alert."""
    type: str        # "positive" | "negative"
    dimension: str
    period: str
    tag: str
    level: int       # 30 | 50
    star_name: str


@dataclass
class DimensionScores:
    """Complete scoring output for one dimension."""
    dimension: str
    label: str
    lifetime: list[ScorePoint] = field(default_factory=list)
    decade: list[ScorePoint] = field(default_factory=list)
    monthly: list[ScorePoint] = field(default_factory=list)
    alerts: list[Alert] = field(default_factory=list)
    summary_score: float = 0.0


@dataclass
class ScoringResult:
    """Complete scoring output for all dimensions."""
    dimensions: dict[str, DimensionScores] = field(default_factory=dict)
    all_alerts: list[Alert] = field(default_factory=list)


# --- AI pipeline types ---


@dataclass
class UserProfile:
    """User profile data for AI prompt building."""
    name: str | None
    birth_date: date
    birth_hour: str
    birth_hour_label: str
    gender: str
    gender_label: str
    current_age: int
    nam_xem: int

    @property
    def display_name(self) -> str:
        return self.name if self.name else "Bạn"


@dataclass
class LasoMetadata:
    """Lá số metadata extracted from scraper output."""
    nam: str          # "Giáp Tuất"
    menh: str         # "Mộc"
    cuc: str          # "Thủy Nhị Cục"
    am_duong: str     # "Dương Nam"
    cung_menh: str    # Cung name where Mệnh resides


@dataclass
class InterpretationResult:
    """Complete AI interpretation output."""
    overview: str
    dimensions: dict[str, str] = field(default_factory=dict)
    errors: dict[str, str] = field(default_factory=dict)
    token_usage: dict[str, tuple[int, int]] = field(default_factory=dict)

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def completed_count(self) -> int:
        return len(self.dimensions)
