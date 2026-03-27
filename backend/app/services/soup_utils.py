import logging
import unicodedata

logger = logging.getLogger(__name__)


def _normalize(text):
    """Normalize Unicode text to NFC form for consistent comparison."""
    return unicodedata.normalize("NFC", text)


def try_get_text(soup, selector, default=""):
    el = soup.select_one(selector)
    if el is None:
        return default
    return el.text


def find_metadata_field(soup, label, container_selector="div.thien-ban", default=None):
    container = soup.select_one(container_selector)
    if not container:
        logger.warning("Container '%s' not found", container_selector)
        return default

    label_nfc = _normalize(label)
    label_search = _normalize(label.rstrip(":").strip())

    # Strategy 1: label + value in same <p> tag (tuvi.cohoc style)
    for p in container.find_all("p"):
        text = _normalize(p.get_text())
        if label_nfc in text:
            span = p.find("span")
            if span:
                return _normalize(span.get_text(strip=True))
            value = text.replace(label_nfc, "").strip()
            if value:
                return value

    # Strategy 2: label in <td>, value in sibling <td> (tuvi.vn style)
    for td in container.find_all("td"):
        td_text = _normalize(td.get_text(strip=True))
        if label_search in td_text:
            next_td = td.find_next_sibling("td")
            if next_td:
                span = next_td.find("span")
                if span:
                    return _normalize(span.get_text(strip=True))
                return _normalize(next_td.get_text(strip=True))

    logger.warning("Metadata field '%s' not found", label)
    return default


def to_string(text: str):
    text = unicodedata.normalize("NFC", text)
    # Remove dashes and plus signs first
    text = text.replace("-", " ").replace("+", " ")
    # Split on whitespace (handles spaces, newlines, tabs)
    parts = text.split()
    # Filter out empty strings
    parts = [p.strip() for p in parts if p.strip()]
    return " ".join(parts)
