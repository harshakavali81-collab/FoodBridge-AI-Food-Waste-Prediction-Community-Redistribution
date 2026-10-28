"""HTML and asset contract checks for the static public portfolio bundle."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse,unquote
import pytest

ROOT=Path(__file__).resolve().parents[1]
PAGES=[
    ROOT/"docs/index.html",
    ROOT/"docs/demo.html",
    ROOT/"docs/launch-readiness.html",
    ROOT/"portfolio/index.html",
]

class LocalRefs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs=[]
        self.images=0
        self.has_title=False
        self.has_description=False
    def handle_starttag(self,tag,attrs):
        props=dict(attrs)
        if tag=="title":self.has_title=True
        if tag=="meta" and props.get("name")=="description" and props.get("content"):
            self.has_description=True
        if tag=="img":
            self.images+=1
            if not props.get("alt"):raise AssertionError("Missing image alternative text")
        for attr in ("href","src"):
            value=props.get(attr)
            if value:self.refs.append(value)

@pytest.mark.parametrize("path",PAGES,ids=lambda p:p.relative_to(ROOT).as_posix())
def test_page_metadata_and_local_paths(path):
    assert path.is_file()
    parser=LocalRefs()
    parser.feed(path.read_text(encoding="utf-8"))
    assert parser.has_title and parser.has_description
    for ref in parser.refs:
        target=urlparse(ref)
        if target.scheme or target.netloc or not target.path:
            continue
        resolved=(path.parent/unquote(target.path)).resolve()
        assert resolved.is_relative_to(ROOT),f"Local reference escapes repository: {ref}"
        assert resolved.exists(),f"Broken local link in {path.name}: {ref}"

def test_ten_original_svgs_and_external_backend_isolation():
    assets=sorted((ROOT/"docs/assets").glob("*.svg"))
    assert len(assets)==10
    assert all(f.read_text(encoding="utf-8").lstrip().startswith("<svg") for f in assets)
    demo=(ROOT/"docs/demo.html").read_text(encoding="utf-8")
    assert "No real" in demo and "simulation" in demo.lower()
    assert "api/v1" not in demo and "API_KEY" not in demo
    assert "localStorage" not in (ROOT/"frontend/src/api/client.js").read_text(encoding="utf-8")
