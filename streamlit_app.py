"""trace-to-eval-cli -- live demo (Streamlit Community Cloud).

Reads the committed eval report under reports/ttec_v0_1_demo.json and shows a
ranked pass/fail view of deterministic trace-eval cases: which cases failed,
which checks broke, and the worst offender. No network, no secrets -- runs
entirely off the committed fixture report.

Deploy: Streamlit Community Cloud -> New app -> repo AthenaTheOwl/trace-to-eval-cli,
branch main, main file streamlit_app.py.
"""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from trace_to_eval_cli.runner import summarize_report

REPO = Path(__file__).resolve().parent
REPORT = REPO / "reports" / "ttec_v0_1_demo.json"

st.set_page_config(page_title="trace-to-eval-cli -- eval report", layout="wide")
st.title("trace-to-eval-cli")
st.caption(
    "deterministic agent-trace eval. each case runs offline checks "
    "(text present/absent, citation span, allowed tool call, required refusal) "
    "against a langgraph trace fixture, ranked failing-first."
)

if not REPORT.exists():
    st.warning(f"no report found at {REPORT.relative_to(REPO).as_posix()}")
    st.stop()

report = json.loads(REPORT.read_text(encoding="utf-8"))
view = summarize_report(report)
summary = view["summary"]

st.subheader(f"run: {view['run_id']}  (generated {view['generated_at']})")

c1, c2, c3 = st.columns(3)
c1.metric("cases", summary["total"])
c2.metric("failing", summary["failed"], help="cases with at least one failed check")
c3.metric("pass rate", f"{view['pass_rate_pct']}%")

status_options = ["all", "failed", "passed", "skipped"]
choice = st.radio("filter by status", status_options, horizontal=True)

rows = view["cases"]
if choice != "all":
    rows = [r for r in rows if r["status"] == choice]

if not rows:
    st.info(f"no cases with status '{choice}'.")
else:
    st.dataframe(
        [
            {
                "rank": i,
                "case": r["case_id"],
                "suite": r["suite"],
                "status": r["status"],
                "checks ok": f"{r['checks_passed']}/{r['checks_total']}",
                "failing": r["checks_failed"],
                "trace": r["trace_id"],
            }
            for i, r in enumerate(rows, start=1)
        ],
        use_container_width=True,
        hide_index=True,
    )

st.info(f"**finding:** {view['headline']}")

failing_cases = [r for r in view["cases"] if r["status"] == "failed"]
if failing_cases:
    with st.expander("failing checks for the worst case", expanded=True):
        worst = failing_cases[0]
        st.markdown(f"**{worst['case_id']}** ({worst['suite']}) -- trace `{worst['trace_id']}`")
        for line in worst["failing_checks"]:
            st.markdown(f"- {line}")

st.caption(
    "v0.1 ships one langgraph fixture suite (vendor-approval / vendor-block / guardrail). "
    "the checks + scoring live in `trace_to_eval_cli/`; this page reads the committed "
    "`reports/ttec_v0_1_demo.json`. repo: github.com/AthenaTheOwl/trace-to-eval-cli"
)
