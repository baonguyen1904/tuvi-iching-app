"""AI Luận Giải Engine — KB loading, prompt building, Claude API orchestration."""

from dataclasses import dataclass, field
from pathlib import Path


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
