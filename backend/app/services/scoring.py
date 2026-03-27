"""Scoring engine — transforms LasoData into scored dimensions with alerts."""

import logging
from pathlib import Path

from openpyxl import load_workbook
from slugify import slugify

from app.constants import DIMENSIONS
from app.models.schemas import (
    StarRow,
    ScorePoint,
    Alert,
    DimensionScores,
    ScoringResult,
)

logger = logging.getLogger(__name__)

# Dimension columns that have alert tag columns in the xlsx.
# van_menh has NO alerts so it has no tag columns.
_ALERT_DIMENSIONS = [d for d in DIMENSIONS if d != "van_menh"]


class ScoringEngine:
    """Stateless scoring calculator. Load xlsx once, reuse across requests."""

    def __init__(self, xlsx_path: str = "data/laso_points.xlsx"):
        self._star_table: dict[str, StarRow] = self._load_star_table(xlsx_path)

    def _load_star_table(self, path: str) -> dict[str, StarRow]:
        wb = load_workbook(path, read_only=True, data_only=True)
        ws = wb["laso_points"]

        # Read header row to build column index
        rows = ws.iter_rows(values_only=True)
        header = [str(h).strip() if h else "" for h in next(rows)]
        col = {name: idx for idx, name in enumerate(header) if name}

        def _safe_get(row: tuple, idx: int):
            """Safely get a value from a row tuple, returning None if out of range."""
            return row[idx] if idx < len(row) else None

        table: dict[str, StarRow] = {}

        for row_vals in rows:
            sao_raw = _safe_get(row_vals, col["sao"])
            if sao_raw is None:
                continue

            slug = slugify(str(sao_raw).lower())
            if slug in table:
                logger.warning("Duplicate star slug '%s' (name: %s) — keeping first", slug, sao_raw)
                continue

            point_val = _safe_get(row_vals, col["point"])
            point = int(point_val) if point_val is not None else 0

            # Build dimension weights — empty/NaN -> 1.0
            weights: dict[str, float] = {}
            for dim in DIMENSIONS:
                val = _safe_get(row_vals, col[dim]) if dim in col else None
                if val is None or val == "":
                    weights[dim] = 1.0
                else:
                    try:
                        weights[dim] = float(val)
                    except (ValueError, TypeError):
                        weights[dim] = 1.0

            # Build pct_fvg
            pct_fvg: dict[int, str | None] = {}
            for level in (30, 50):
                fvg_col = f"pct_fvg_{level}"
                if fvg_col in col:
                    val = _safe_get(row_vals, col[fvg_col])
                    if val and str(val).strip() in ("pos", "neg"):
                        pct_fvg[level] = str(val).strip()
                    else:
                        pct_fvg[level] = None
                else:
                    pct_fvg[level] = None

            # Build alert tags per dimension per level
            alert_tags: dict[str, dict[int, str | None]] = {}
            for dim in _ALERT_DIMENSIONS:
                dim_tags: dict[int, str | None] = {}
                for level in (30, 50):
                    tag_col = f"{dim}_tag_{level}"
                    if tag_col in col:
                        val = _safe_get(row_vals, col[tag_col])
                        if val and str(val).strip():
                            dim_tags[level] = str(val).strip()
                        else:
                            dim_tags[level] = None
                    else:
                        dim_tags[level] = None
                alert_tags[dim] = dim_tags

            table[slug] = StarRow(
                slug=slug,
                name=str(sao_raw),
                point=point,
                weights=weights,
                alert_tags=alert_tags,
                pct_fvg=pct_fvg,
            )

        wb.close()
        logger.info("Loaded %d stars from %s", len(table), path)
        return table

    def _build_raw_scores(
        self, cungs: list, dim: str
    ) -> dict[str, tuple[float, float]]:
        """Calculate raw pos/neg scores per cung for a dimension.

        Args:
            cungs: List of Cung (or any object with .name and .stars[].slug).
            dim: Dimension key (e.g., "su_nghiep").

        Returns:
            Dict mapping lowered cung name -> (raw_pos, raw_neg).
        """
        result: dict[str, tuple[float, float]] = {}

        for cung in cungs:
            raw_pos = 0.0
            raw_neg = 0.0

            for star in cung.stars:
                row = self._star_table.get(star.slug)
                if row is None:
                    logger.warning(
                        "Star not found in table: slug='%s' (cung='%s')",
                        star.slug,
                        cung.name,
                    )
                    continue

                weight = row.weights.get(dim, 1.0)
                contribution = row.point * weight

                if row.point > 0:
                    raw_pos += contribution
                else:
                    raw_neg += contribution

            result[cung.name.lower()] = (raw_pos, raw_neg)

        return result
