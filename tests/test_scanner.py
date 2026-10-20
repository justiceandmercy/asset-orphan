import os
import tempfile
from pathlib import Path

from asset_orphan.scanner import scan


def _write(d, name, content=""):
    p = os.path.join(d, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(content)
    return p


def test_orphan_detected():
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "img"))
        with open(os.path.join(d, "img", "unused.png"), "wb") as f:
            f.write(b"\x89PNG\r\n")
        _write(d, "index.html", "<html></html>")
        res = scan(Path(d))
        assert "img/unused.png" in res.orphans


def test_used_asset_not_orphan():
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "img"))
        with open(os.path.join(d, "img", "logo.png"), "wb") as f:
            f.write(b"\x89PNG\r\n")
        _write(d, "index.html", '<img src="img/logo.png">')
        res = scan(Path(d))
        assert res.orphans == set()
        assert "img/logo.png" in res.used


def test_skips_node_modules():
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "node_modules", "pkg"), exist_ok=True)
        with open(os.path.join(d, "node_modules", "pkg", "x.png"), "wb") as f:
            f.write(b"x")
        res = scan(Path(d))
        assert res.assets == set()
