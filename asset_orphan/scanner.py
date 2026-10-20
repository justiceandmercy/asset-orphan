"""Scan a codebase for orphaned asset files."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Set


ASSET_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".bmp",
    ".tif", ".tiff", ".avif",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".mp4", ".mov", ".webm", ".mp3", ".wav", ".ogg", ".pdf",
}

SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", "__pycache__", ".next",
    "vendor", "coverage", ".venv", "venv", ".idea", ".vscode", ".cache",
}


@dataclass
class ScanResult:
    assets: Set[str] = field(default_factory=set)
    used: Set[str] = field(default_factory=set)

    @property
    def orphans(self) -> Set[str]:
        return self.assets - self.used


def _iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            yield Path(dirpath) / fn


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def scan(root: Path) -> ScanResult:
    root = Path(root).resolve()
    result = ScanResult()

    asset_paths = []
    corpus_parts = []

    for p in _iter_files(root):
        if p.suffix.lower() in ASSET_EXTENSIONS:
            asset_paths.append(p)
            result.assets.add(p.relative_to(root).as_posix())
        else:
            corpus_parts.append(_read_text(p))

    corpus = "\n".join(corpus_parts).lower()

    for ap in asset_paths:
        rel = ap.relative_to(root).as_posix()
        basename = ap.name
        needles = {rel.lower(), basename.lower()}
        if any(n in corpus for n in needles):
            result.used.add(rel)

    return result
