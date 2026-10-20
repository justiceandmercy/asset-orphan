"""CLI for asset-orphan."""
from __future__ import annotations

try:
    from .scanner import scan, ScanResult
except ImportError:  # pragma: no cover - flat execution
    from scanner import scan, ScanResult

import argparse
import json
import sys
from pathlib import Path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="asset-orphan",
        description="Find asset files (images, fonts, media) never referenced in source code.",
    )
    parser.add_argument("path", nargs="?", default=".", help="root directory to scan")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument(
        "--exit-code", action="store_true", help="exit 1 if orphans found"
    )
    args = parser.parse_args(argv)

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    result = scan(root)

    if args.format == "json":
        print(json.dumps(sorted(result.orphans), indent=2))
    else:
        print(f"Scanned: {root}")
        print(f"Assets: {len(result.assets)}, used: {len(result.used)}, orphans: {len(result.orphans)}")
        print()
        if result.orphans:
            print("Orphan assets:")
            for o in sorted(result.orphans):
                print(f"  {o}")
        else:
            print("No orphan assets found.")

    if args.exit_code and result.orphans:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
