from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from trace_to_eval_cli.io import load_json
from trace_to_eval_cli.paths import DEFAULT_CASE_PATH, DEFAULT_REPORT_PATH, DEFAULT_TRACES_DIR
from trace_to_eval_cli.runner import build_report


def main() -> int:
    expected = load_json(DEFAULT_REPORT_PATH)
    report = build_report(DEFAULT_CASE_PATH, DEFAULT_TRACES_DIR)
    if report != expected:
        print("TTEC_DOGFOOD_FAILED: built report differs from checked artifact", file=sys.stderr)
        return 1
    print("TTEC_OK: dogfood report matches checked artifact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
