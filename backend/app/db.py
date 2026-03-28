"""SQLite database layer for profile caching."""

import hashlib
import json
import logging
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "tuvi.db"

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS profiles (
    id TEXT PRIMARY KEY,
    name TEXT,
    birth_date TEXT NOT NULL,
    birth_hour TEXT NOT NULL,
    gender TEXT NOT NULL,
    nam_xem INTEGER NOT NULL DEFAULT 2026,
    metadata JSON,
    cung_lifetime JSON,
    cung_10yrs JSON,
    cung_12months JSON,
    scores JSON,
    alerts JSON,
    overview_summary TEXT,
    interpretations JSON,
    status TEXT DEFAULT 'processing',
    current_step TEXT,
    ai_progress INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_profiles_cache ON profiles(birth_date, birth_hour, gender, nam_xem);
"""


def init_db(db_path: Optional[Path] = None):
    """Create tables if they don't exist."""
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.executescript(_CREATE_TABLE)
    conn.close()
    logger.info("Database initialized at %s", path)


@contextmanager
def get_conn(db_path: Optional[Path] = None):
    path = db_path or DB_PATH
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def make_profile_id(birth_date: str, birth_hour: str, gender: str, nam_xem: int) -> str:
    """Generate deterministic cache key."""
    raw = f"{birth_date}|{birth_hour}|{gender}|{nam_xem}"
    return hashlib.sha256(raw.encode()).hexdigest()[:12]


def find_cached(birth_date: str, birth_hour: str, gender: str, nam_xem: int) -> Optional[dict]:
    """Find completed profile with same birth data."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM profiles WHERE birth_date=? AND birth_hour=? AND gender=? AND nam_xem=? AND status='completed' LIMIT 1",
            (birth_date, birth_hour, gender, nam_xem),
        ).fetchone()
        return dict(row) if row else None


def create_profile(profile_id: str, name: str, birth_date: str, birth_hour: str, gender: str, nam_xem: int):
    with get_conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO profiles (id, name, birth_date, birth_hour, gender, nam_xem, status, current_step) VALUES (?, ?, ?, ?, ?, ?, 'processing', 'scraping_cohoc')",
            (profile_id, name, birth_date, birth_hour, gender, nam_xem),
        )


def update_step(profile_id: str, step: str, ai_progress: int = 0):
    with get_conn() as conn:
        conn.execute(
            "UPDATE profiles SET current_step=?, ai_progress=? WHERE id=?",
            (step, ai_progress, profile_id),
        )


def save_scrape_data(profile_id: str, metadata: dict, cung_lifetime: list, cung_10yrs: list, cung_12months: list):
    with get_conn() as conn:
        conn.execute(
            "UPDATE profiles SET metadata=?, cung_lifetime=?, cung_10yrs=?, cung_12months=? WHERE id=?",
            (json.dumps(metadata, ensure_ascii=False),
             json.dumps(cung_lifetime, ensure_ascii=False),
             json.dumps(cung_10yrs, ensure_ascii=False),
             json.dumps(cung_12months, ensure_ascii=False),
             profile_id),
        )


def save_scores(profile_id: str, scores: dict, alerts: list):
    with get_conn() as conn:
        conn.execute(
            "UPDATE profiles SET scores=?, alerts=? WHERE id=?",
            (json.dumps(scores, ensure_ascii=False),
             json.dumps(alerts, ensure_ascii=False),
             profile_id),
        )


def save_ai_result(profile_id: str, overview: str, interpretations: dict):
    with get_conn() as conn:
        conn.execute(
            "UPDATE profiles SET overview_summary=?, interpretations=?, status='completed', completed_at=? WHERE id=?",
            (overview,
             json.dumps(interpretations, ensure_ascii=False),
             datetime.now(timezone.utc).isoformat(),
             profile_id),
        )


def set_error(profile_id: str, error_message: str):
    with get_conn() as conn:
        conn.execute(
            "UPDATE profiles SET status='error', error_message=? WHERE id=?",
            (error_message, profile_id),
        )


def get_profile(profile_id: str) -> Optional[dict]:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM profiles WHERE id=?", (profile_id,)).fetchone()
        return dict(row) if row else None


def get_status(profile_id: str) -> Optional[dict]:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, status, current_step, ai_progress, error_message FROM profiles WHERE id=?",
            (profile_id,),
        ).fetchone()
        return dict(row) if row else None
