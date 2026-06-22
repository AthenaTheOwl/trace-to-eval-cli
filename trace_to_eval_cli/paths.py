from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CASE_PATH = REPO_ROOT / "examples" / "eval-cases" / "ttec_smoke.yaml"
DEFAULT_TRACES_DIR = REPO_ROOT / "examples" / "traces" / "canonical"
DEFAULT_REPORT_PATH = REPO_ROOT / "reports" / "ttec_v0_1_smoke.json"
DEFAULT_MARKDOWN_REPORT_PATH = REPO_ROOT / "reports" / "ttec_v0_1_smoke.md"
DEFAULT_RUN_ID = "ttec-v0.1-smoke"
DEFAULT_GENERATED_AT = "2026-06-22T00:00:00Z"

