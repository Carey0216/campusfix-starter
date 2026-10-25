from pathlib import Path

def test_index_title():
    html = Path("templates/index.html").read_text(encoding="utf-8")
    assert "<h1>CampusFix-20252044</h1>" in html
