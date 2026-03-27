"""AI Luận Giải Engine — KB loading, prompt building, Claude API orchestration.

Integration with FastAPI:

In main.py lifespan:
    engine = AIEngine(kb_dir="knowledge_base", api_key=os.environ["ANTHROPIC_API_KEY"])
    app.state.ai_engine = engine

In router:
    engine = request.app.state.ai_engine
    result = await engine.generate_all(user, metadata, laso, scoring, progress_callback)
    # Store result in SQLite
    # Update profile status to "completed"
"""

import asyncio
import logging
from dataclasses import dataclass, field
from pathlib import Path

import anthropic

from app.constants import DIMENSION_LABELS, HOUSE_WEIGHTS
from app.models.schemas import (
    ScorePoint, Alert, DimensionScores, ScoringResult,
    UserProfile, LasoMetadata, InterpretationResult,
)

logger = logging.getLogger(__name__)

# --- API Configuration ---

MAX_RETRIES = 3
RETRY_DELAYS = [2, 5, 10]  # seconds
TIMEOUT_PER_CALL = 60

RETRYABLE_ERRORS = (
    anthropic.RateLimitError,
    anthropic.APIConnectionError,
    anthropic.InternalServerError,
)


# --- Knowledge Base ---


class KBLoadError(Exception):
    """Raised when KB files cannot be loaded."""
    pass


@dataclass
class KnowledgeBase:
    core: dict[str, str] = field(default_factory=dict)
    dimensions: dict[str, str] = field(default_factory=dict)
    stars: dict[str, str] = field(default_factory=dict)
    examples: dict[str, str] = field(default_factory=dict)


REQUIRED_CORE = ["scoring_rules", "alert_interpretation", "tone_guidelines"]
REQUIRED_DIMENSIONS = ["su_nghiep", "tien_bac", "hon_nhan", "suc_khoe", "dat_dai", "hoc_tap", "con_cai"]
REQUIRED_STARS = ["chinh_tinh", "phu_tinh"]


def _load_md_files(directory: Path) -> dict[str, str]:
    """Load all .md files from a directory into a dict keyed by stem."""
    result = {}
    if directory.is_dir():
        for f in sorted(directory.glob("*.md")):
            result[f.stem] = f.read_text(encoding="utf-8")
    return result


def load_kb(kb_dir: str) -> KnowledgeBase:
    """Load all KB markdown files. Raises KBLoadError if required files missing."""
    base = Path(kb_dir)
    if not base.is_dir():
        raise KBLoadError(f"KB directory not found: {kb_dir}")

    kb = KnowledgeBase()

    # Load core
    kb.core = _load_md_files(base / "core")
    for req in REQUIRED_CORE:
        if req not in kb.core:
            raise KBLoadError(f"Missing required core KB file: {req}.md")

    # Load dimensions
    kb.dimensions = _load_md_files(base / "dimensions")
    for req in REQUIRED_DIMENSIONS:
        if req not in kb.dimensions:
            raise KBLoadError(f"Missing required dimension KB file: {req}.md")

    # Load stars
    kb.stars = _load_md_files(base / "stars")
    for req in REQUIRED_STARS:
        if req not in kb.stars:
            raise KBLoadError(f"Missing required stars KB file: {req}.md")

    # Load examples (optional — no required files)
    examples_dir = base / "examples" / "approved_outputs"
    kb.examples = _load_md_files(examples_dir)

    return kb


# --- Score & Alert Formatting ---


def format_scores_table(points: list[ScorePoint], header: str = "Giai đoạn") -> str:
    """Format score points as markdown table."""
    lines = [
        f"| {header} | Dương | Âm | TB |",
        f"|{'---' * len(header)}|-------|-----|-----|",
    ]
    for p in points:
        lines.append(f"| {p.period} | {p.duong:.2f} | {p.am:.2f} | {p.tb:.2f} |")
    return "\n".join(lines)


def format_alerts(alerts: list[Alert]) -> str:
    """Format alerts as readable text with 🔺🔻 markers, sorted by level desc."""
    if not alerts:
        return "Không có cảnh báo đặc biệt."

    sorted_alerts = sorted(alerts, key=lambda a: a.level, reverse=True)
    lines = []
    for a in sorted_alerts:
        icon = "🔺" if a.type == "positive" else "🔻"
        lines.append(f"{icon} {a.period} (Level {a.level}): {a.tag} [sao: {a.star_name}]")
    return "\n".join(lines)


# --- Output Validation ---

FORBIDDEN_PHRASES = [
    "sẽ gặp họa",
    "chắc chắn sẽ",
    "tuyệt đối",
]


def validate_output(text: str, dimension: str) -> list[str]:
    """Validate AI output. Returns list of warnings (empty = pass)."""
    warnings = []

    # Check forbidden phrases
    for phrase in FORBIDDEN_PHRASES:
        if phrase in text:
            warnings.append(f"TONE: Contains forbidden phrase '{phrase}'")

    # Check disclaimer
    stripped = text.strip()
    if not stripped.endswith("*"):
        warnings.append("MISSING: No disclaimer at end (should end with italic *tham khảo* text)")

    # Check length
    if len(text) < 200:
        warnings.append(f"SHORT: Output under 200 chars ({len(text)} chars)")
    if len(text) > 5000:
        warnings.append(f"LONG: Output over 5000 chars ({len(text)} chars)")

    # Check for ## headings
    if "## " not in text:
        warnings.append("STRUCTURE: No ## headings found in output")

    return warnings


# --- Dimension → Primary Cung Mapping ---

DIMENSION_PRIMARY_CUNGS: dict[str, list[str]] = {
    "su_nghiep": ["quan lộc", "mệnh"],
    "tien_bac": ["tài bạch", "mệnh"],
    "hon_nhan": ["phu thê", "mệnh"],
    "suc_khoe": ["tật ách", "phúc đức"],
    "dat_dai": ["điền trạch", "tài bạch"],
    "hoc_tap": ["mệnh", "quan lộc"],
    "con_cai": ["tử tức", "phúc đức"],
}

# Mapping from unaccented cung names (from laso JSON) to Vietnamese
_CUNG_NAME_MAP: dict[str, str] = {
    "menh": "mệnh",
    "phu mau": "phụ mẫu",
    "phuc duc": "phúc đức",
    "dien trach": "điền trạch",
    "quan loc": "quan lộc",
    "no boc": "nô bộc",
    "thien di": "thiên di",
    "tat ach": "tật ách",
    "tai bach": "tài bạch",
    "tu tuc": "tử tức",
    "phu the": "phu thê",
    "huynh de": "huynh đệ",
}


def _normalize_cung_name(name: str) -> str:
    """Normalize cung name from laso JSON to Vietnamese lowercase."""
    return _CUNG_NAME_MAP.get(name.lower(), name.lower())


# --- AIEngine ---


class AIEngine:
    """Stateless AI text generator. Load KB once, reuse across requests."""

    def __init__(self, kb_dir: str, api_key: str):
        self._kb: KnowledgeBase = load_kb(kb_dir)
        self._api_key = api_key
        self._client = anthropic.AsyncAnthropic(api_key=api_key)

    async def _call_claude(self, system: str, user_msg: str) -> tuple[str, int, int]:
        """Call Claude API with retry logic. Returns (text, input_tokens, output_tokens)."""
        for attempt in range(MAX_RETRIES):
            try:
                response = await self._client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=2000,
                    temperature=0.7,
                    system=system,
                    messages=[{"role": "user", "content": user_msg}],
                )
                text = response.content[0].text
                return text, response.usage.input_tokens, response.usage.output_tokens
            except RETRYABLE_ERRORS as e:
                if attempt == MAX_RETRIES - 1:
                    raise
                delay = RETRY_DELAYS[attempt]
                logger.warning(
                    "Claude API error (attempt %d/%d): %s. Retrying in %ds...",
                    attempt + 1, MAX_RETRIES, e, delay,
                )
                await asyncio.sleep(delay)
        # Should not reach here
        raise RuntimeError("Unexpected: exhausted retries without raising")

    async def generate_dimension(
        self,
        dimension: str,
        user: UserProfile,
        metadata: LasoMetadata,
        laso: dict,
        dim_scores: DimensionScores,
    ) -> str:
        """Generate luận giải for a single dimension."""
        system, user_msg = self._build_dimension_prompt(
            dimension, user, metadata, laso, dim_scores
        )
        text, input_tokens, output_tokens = await self._call_claude(system, user_msg)
        logger.info(
            "Generated %s: %d input tokens, %d output tokens",
            dimension, input_tokens, output_tokens,
        )

        # Validate output (log warnings, don't block)
        warnings = validate_output(text, dimension)
        for w in warnings:
            logger.warning("Validation [%s]: %s", dimension, w)

        return text

    async def generate_overview(
        self,
        user: UserProfile,
        metadata: LasoMetadata,
        scoring: ScoringResult,
    ) -> str:
        """Generate overview summary across all dimensions."""
        system, user_msg = self._build_overview_prompt(user, metadata, scoring)
        text, input_tokens, output_tokens = await self._call_claude(system, user_msg)
        logger.info(
            "Generated overview: %d input tokens, %d output tokens",
            input_tokens, output_tokens,
        )
        return text

    async def generate_all(
        self,
        user: UserProfile,
        metadata: LasoMetadata,
        laso: dict,
        scoring: ScoringResult,
        progress_callback=None,
    ) -> InterpretationResult:
        """Generate overview + 7 dimensions concurrently. Main entry point."""
        DIMS = ["su_nghiep", "tien_bac", "hon_nhan", "suc_khoe", "dat_dai", "hoc_tap", "con_cai"]

        # Build task dict: key → coroutine
        task_keys = ["overview"] + DIMS
        coros = [self.generate_overview(user, metadata, scoring)]
        for dim in DIMS:
            coros.append(
                self.generate_dimension(dim, user, metadata, laso, scoring.dimensions[dim])
            )

        results = await asyncio.gather(*coros, return_exceptions=True)

        interpretation = InterpretationResult(
            overview="",
            dimensions={},
            errors={},
            token_usage={},
        )

        completed = 0
        for key, result in zip(task_keys, results):
            completed += 1
            if isinstance(result, Exception):
                interpretation.errors[key] = f"{type(result).__name__}: {str(result)}"
                logger.error("Failed to generate %s: %s", key, result)
            elif key == "overview":
                interpretation.overview = result
            else:
                interpretation.dimensions[key] = result

            if progress_callback:
                await progress_callback(completed, 8)

        return interpretation

    def _get_stars_in_cungs(self, laso: dict, cung_names: list[str]) -> list[str]:
        """Get star names from laso data for given cung names."""
        stars = []
        cung_list = laso.get("cung", [])
        for cung in cung_list:
            normalized = _normalize_cung_name(cung.get("name", ""))
            if normalized in cung_names:
                for star in cung.get("stars", []):
                    stars.append(star.get("name", ""))
        return stars

    def _filter_stars_for_dimension(self, dimension: str, laso: dict) -> str:
        """Filter chinh_tinh.md content for stars in dimension's primary cungs."""
        primary_cungs = DIMENSION_PRIMARY_CUNGS.get(dimension, [])
        star_names = self._get_stars_in_cungs(laso, primary_cungs)

        if not star_names:
            return ""

        # Extract base star names (remove variant like "(B)", "(D)")
        base_names = set()
        for name in star_names:
            # "Tu Vi (B)" → "Tử Vi" — match by checking chinh_tinh content
            base = name.split("(")[0].strip()
            base_names.add(base)

        # Filter chinh_tinh content to relevant sections
        chinh_tinh = self._kb.stars.get("chinh_tinh", "")
        relevant_sections = []
        current_section = []
        current_star = None

        for line in chinh_tinh.split("\n"):
            if line.startswith("## "):
                # Save previous section if relevant
                if current_star and current_section:
                    relevant_sections.append("\n".join(current_section))
                current_star = line[3:].strip()
                current_section = [line]
                # Check if any base_name is a substring of the star heading
                is_relevant = any(
                    base.lower() in current_star.lower() or current_star.lower() in base.lower()
                    for base in base_names
                )
                if not is_relevant:
                    current_star = None
                    current_section = []
            elif current_star:
                current_section.append(line)

        # Don't forget last section
        if current_star and current_section:
            relevant_sections.append("\n".join(current_section))

        return "\n\n".join(relevant_sections) if relevant_sections else ""

    def _build_dimension_prompt(
        self,
        dimension: str,
        user: UserProfile,
        metadata: LasoMetadata,
        laso: dict,
        dim_scores: DimensionScores,
    ) -> tuple[str, str]:
        """Build (system_message, user_message) for a dimension prompt."""
        label = DIMENSION_LABELS.get(dimension, dimension)

        # --- System message ---
        system_parts = [
            # Role definition
            "[ROLE DEFINITION]\n"
            "Bạn là tư vấn viên luận giải tử vi chuyên nghiệp, sử dụng hệ thống "
            "Chánh Ngã Đồ (Tử Vi Đẩu Số + scoring analytics). Nhiệm vụ: viết luận "
            f"giải cá nhân hóa cho lĩnh vực {label} dựa trên data được cung cấp.",

            # Rules
            "[RULES — NON-NEGOTIABLE]\n"
            "1. Chỉ nói về data được cung cấp — KHÔNG bịa đặt\n"
            "2. Ngôn ngữ tích cực, empowering — giọng văn \"anh trai khuyên em\"\n"
            "3. Mỗi cảnh báo 🔻 PHẢI đi kèm lời khuyên cụ thể\n"
            "4. Dùng \"cần thận trọng\" thay vì \"sẽ gặp họa\"\n"
            "5. Kết thúc bằng disclaimer\n"
            "6. Viết tiếng Việt tự nhiên, không quá trang trọng, không thần bí",

            # Core KB
            f"[KNOWLEDGE BASE — CORE]\n{self._kb.core['scoring_rules']}\n\n"
            f"{self._kb.core['alert_interpretation']}",

            # Tone KB
            f"[KNOWLEDGE BASE — TONE]\n{self._kb.core['tone_guidelines']}",

            # Dimension KB
            f"[KNOWLEDGE BASE — DIMENSION: {label}]\n{self._kb.dimensions[dimension]}",
        ]

        # Filtered star content
        star_content = self._filter_stars_for_dimension(dimension, laso)
        if star_content:
            system_parts.append(f"[RELEVANT STARS]\n{star_content}")

        system = "\n\n".join(system_parts)

        # --- User message ---
        # Primary cungs and their stars
        primary_cungs = DIMENSION_PRIMARY_CUNGS.get(dimension, [])
        stars_in_cungs = self._get_stars_in_cungs(laso, primary_cungs)
        stars_list = ", ".join(stars_in_cungs) if stars_in_cungs else "N/A"

        primary_cung_label = primary_cungs[0].title() if primary_cungs else dimension

        user_parts = [
            f"[USER DATA]\n"
            f"- Tên: {user.display_name}\n"
            f"- Sinh: {user.birth_date} ({metadata.nam}), {user.birth_hour_label}, {user.gender_label}\n"
            f"- Tuổi hiện tại: {user.current_age}\n"
            f"- Cung Mệnh: {metadata.cung_menh} — Mệnh {metadata.menh}\n"
            f"- Cung {primary_cung_label}: {stars_list}",

            f"[SCORE DATA — {label}]\n"
            f"### Cả đời (mốc 10 năm):\n{format_scores_table(dim_scores.lifetime)}",

            f"### 10 năm hiện tại:\n{format_scores_table(dim_scores.decade, header='Năm')}",

            f"### 12 tháng ({user.nam_xem}):\n{format_scores_table(dim_scores.monthly, header='Tháng')}",

            f"[ALERTS — {label}]\n{format_alerts(dim_scores.alerts)}",
        ]

        # Example output if available
        example_key = f"sample_{dimension}"
        if example_key in self._kb.examples:
            user_parts.append(f"[EXAMPLE OUTPUT]\n{self._kb.examples[example_key]}")

        # Output format instructions
        user_parts.append(
            f"[OUTPUT FORMAT]\n"
            f"Viết luận giải tiếng Việt theo format:\n\n"
            f"## Tổng quan {label}\n"
            f"(3-5 câu nhận xét tổng thể dựa trên pattern cả đời)\n\n"
            f"## Giai đoạn hiện tại\n"
            f"(Phân tích 10 năm hiện tại, xu hướng Dương/Âm)\n\n"
            f"## Các mốc cần chú ý\n"
            f"(Mỗi alert: giải thích tại sao + nên làm gì / tránh gì)\n\n"
            f"## Lời khuyên\n"
            f"(2-3 điều cụ thể, actionable, phù hợp với tuổi {user.current_age})\n\n"
            f"---\n"
            f"*Đây là luận giải tham khảo dựa trên Tử Vi Đẩu Số. "
            f"Mọi quyết định cuối cùng là của bạn.*"
        )

        user_msg = "\n\n".join(user_parts)
        return system, user_msg

    def _build_overview_prompt(
        self,
        user: UserProfile,
        metadata: LasoMetadata,
        scoring: ScoringResult,
    ) -> tuple[str, str]:
        """Build (system_message, user_message) for overview prompt."""
        # --- System message (core KB + tone, no dimension KB, no stars) ---
        system_parts = [
            "[ROLE DEFINITION]\n"
            "Bạn là tư vấn viên luận giải tử vi chuyên nghiệp, sử dụng hệ thống "
            "Chánh Ngã Đồ (Tử Vi Đẩu Số + scoring analytics). Nhiệm vụ: viết tổng "
            "quan vận mệnh dựa trên data được cung cấp.",

            "[RULES — NON-NEGOTIABLE]\n"
            "1. Chỉ nói về data được cung cấp — KHÔNG bịa đặt\n"
            "2. Ngôn ngữ tích cực, empowering — giọng văn \"anh trai khuyên em\"\n"
            "3. Mỗi cảnh báo 🔻 PHẢI đi kèm lời khuyên cụ thể\n"
            "4. Dùng \"cần thận trọng\" thay vì \"sẽ gặp họa\"\n"
            "5. Kết thúc bằng disclaimer\n"
            "6. Viết tiếng Việt tự nhiên, không quá trang trọng, không thần bí",

            f"[KNOWLEDGE BASE — CORE]\n{self._kb.core['scoring_rules']}\n\n"
            f"{self._kb.core['alert_interpretation']}",

            f"[KNOWLEDGE BASE — TONE]\n{self._kb.core['tone_guidelines']}",
        ]
        system = "\n\n".join(system_parts)

        # --- User message ---
        dims_to_summarize = [
            "su_nghiep", "tien_bac", "hon_nhan",
            "suc_khoe", "dat_dai", "hoc_tap", "con_cai",
        ]

        dim_summaries = []
        for dim in dims_to_summarize:
            if dim not in scoring.dimensions:
                continue
            ds = scoring.dimensions[dim]
            label = DIMENSION_LABELS.get(dim, dim)
            pos_count = sum(1 for a in ds.alerts if a.type == "positive")
            neg_count = sum(1 for a in ds.alerts if a.type == "negative")
            alert_count = len(ds.alerts)
            dim_summaries.append(
                f"- {label}: TB trung bình {ds.summary_score:.2f}, "
                f"{alert_count} cảnh báo ({pos_count} 🔺, {neg_count} 🔻)"
            )

        user_parts = [
            f"[USER DATA]\n"
            f"- Tên: {user.display_name}\n"
            f"- Sinh: {user.birth_date} ({metadata.nam}), {user.birth_hour_label}, {user.gender_label}\n"
            f"- Tuổi hiện tại: {user.current_age}\n"
            f"- Cung Mệnh: {metadata.cung_menh} — Mệnh {metadata.menh}",

            "[ALL DIMENSION SUMMARIES]\n" + "\n".join(dim_summaries),

            "[OUTPUT FORMAT]\n"
            "Viết tổng quan vận mệnh trong 3-5 câu. Nhận xét bức tranh lớn:\n"
            "- Xu hướng tổng thể\n"
            "- Lĩnh vực mạnh nhất\n"
            "- Lĩnh vực cần chú ý nhất\n"
            "Ngắn gọn, súc tích, gợi mở để người xem muốn đọc chi tiết từng lĩnh vực.\n\n"
            "---\n"
            "*Đây là tổng quan tham khảo dựa trên Tử Vi Đẩu Số. "
            "Mọi quyết định cuối cùng là của bạn.*",
        ]

        user_msg = "\n\n".join(user_parts)
        return system, user_msg
