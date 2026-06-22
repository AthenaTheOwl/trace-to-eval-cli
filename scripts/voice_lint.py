from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANNED_FAIL = {
    "leverage",
    "demonstrate",
    "seamless",
    "cutting-edge",
    "best-in-class",
    "synergy",
}
SCAN_ROOTS = [
    ROOT / "README.md",
    ROOT / "STATUS.md",
    ROOT / "docs",
    ROOT / "reports",
    ROOT / "specs",
    ROOT / "decisions",
]


def main() -> int:
    failures: list[str] = []
    for path in _markdown_files():
        text = path.read_text(encoding="utf-8")
        for word in sorted(BANNED_FAIL):
            pattern = r"\b" + re.escape(word) + r"\b"
            if re.search(pattern, text, flags=re.IGNORECASE):
                failures.append(f"{path.relative_to(ROOT)}: banned word {word}")

    if failures:
        for failure in failures:
            print(f"TTEC_VOICE_FAILED: {failure}", file=sys.stderr)
        return 1
    print("TTEC_OK: markdown voice lint passed")
    return 0


def _markdown_files() -> list[Path]:
    paths: list[Path] = []
    for root in SCAN_ROOTS:
        if root.is_file() and root.suffix == ".md":
            paths.append(root)
        elif root.is_dir():
            paths.extend(root.rglob("*.md"))
    return sorted(paths)


if __name__ == "__main__":
    raise SystemExit(main())

