from bs4 import BeautifulSoup

from app.services.soup_utils import find_metadata_field, to_string, try_get_text


class TestTryGetText:
    def test_found(self):
        html = '<div><span class="val">Hello</span></div>'
        soup = BeautifulSoup(html, "html.parser")
        assert try_get_text(soup, "span.val") == "Hello"

    def test_not_found(self):
        html = "<div></div>"
        soup = BeautifulSoup(html, "html.parser")
        assert try_get_text(soup, "span.val") == ""

    def test_custom_default(self):
        html = "<div></div>"
        soup = BeautifulSoup(html, "html.parser")
        assert try_get_text(soup, "span.val", "N/A") == "N/A"


class TestFindMetadataField:
    def test_cohoc_style_span_in_p(self):
        html = """
        <div class="thien-ban">
            <p>Năm: <span>Đinh Sửu</span></p>
            <p>Mệnh: <span>Giáng Hạ Thủy</span></p>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        assert find_metadata_field(soup, "Năm:") == "Đinh Sửu"
        assert find_metadata_field(soup, "Mệnh:") == "Giáng Hạ Thủy"

    def test_tuvivn_style_sibling_td(self):
        html = """
        <div class="thien-ban">
            <table><tr>
                <td>Âm dương</td>
                <td><span>Dương Nam</span></td>
            </tr></table>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        assert find_metadata_field(soup, "Âm dương:") == "Dương Nam"

    def test_not_found_returns_default(self):
        html = '<div class="thien-ban"><p>Other: <span>val</span></p></div>'
        soup = BeautifulSoup(html, "html.parser")
        assert find_metadata_field(soup, "Missing:") is None
        assert find_metadata_field(soup, "Missing:", default="X") == "X"

    def test_container_not_found(self):
        html = "<div><p>Năm: <span>Val</span></p></div>"
        soup = BeautifulSoup(html, "html.parser")
        assert find_metadata_field(soup, "Năm:") is None

    def test_custom_container(self):
        html = """
        <div class="view-thien-ban">
            <p>Năm: <span>Mậu Thân</span></p>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        result = find_metadata_field(soup, "Năm:", container_selector="div.view-thien-ban")
        assert result == "Mậu Thân"

    def test_unicode_nfc_normalization(self):
        import unicodedata
        label_nfd = unicodedata.normalize("NFD", "Mệnh:")
        html = f'<div class="thien-ban"><p>{label_nfd} <span>Kim</span></p></div>'
        soup = BeautifulSoup(html, "html.parser")
        assert find_metadata_field(soup, "Mệnh:") == "Kim"


class TestToString:
    def test_basic(self):
        assert to_string("  Tử   Vi  ") == "Tử Vi"

    def test_removes_dashes_and_plus(self):
        assert to_string("Thiên - Đồng +") == "Thiên Đồng"

    def test_collapses_whitespace(self):
        assert to_string("Phá\n  Quân") == "Phá Quân"

    def test_nfc_normalization(self):
        import unicodedata
        nfd = unicodedata.normalize("NFD", "Mệnh")
        result = to_string(nfd)
        assert result == unicodedata.normalize("NFC", "Mệnh")

    def test_empty_string(self):
        assert to_string("") == ""
