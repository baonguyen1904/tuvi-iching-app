import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir():
    return FIXTURES_DIR


@pytest.fixture
def cohoc_html(fixtures_dir):
    path = fixtures_dir / "cohoc_result.html"
    if not path.exists():
        pytest.skip("cohoc_result.html fixture not found")
    return path.read_text(encoding="utf-8")


@pytest.fixture
def tuvivn_html(fixtures_dir):
    path = fixtures_dir / "tuvivn_result.html"
    if not path.exists():
        pytest.skip("tuvivn_result.html fixture not found")
    return path.read_text(encoding="utf-8")


@pytest.fixture
def cohoc_expected(fixtures_dir):
    path = fixtures_dir / "cohoc_expected.json"
    if not path.exists():
        pytest.skip("cohoc_expected.json fixture not found")
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture
def tuvivn_expected(fixtures_dir):
    path = fixtures_dir / "tuvivn_expected.json"
    if not path.exists():
        pytest.skip("tuvivn_expected.json fixture not found")
    return json.loads(path.read_text(encoding="utf-8"))
