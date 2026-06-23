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

from trace_to_eval_cli.runner import run_check, summarize_report

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

# ---------------------------------------------------------------------------
# run a check yourself -- drives the REAL engine (trace_to_eval_cli.runner.run_check)
# ---------------------------------------------------------------------------
st.divider()
st.header("run a check on your own trace")
st.caption(
    "edit the agent trace and the checks below, then run them. this calls the real "
    "`run_check(check, trace)` from `trace_to_eval_cli.runner` -- the same engine the cli "
    "and the committed report use. no lookup, no hardcoded result: change the output, "
    "flip a pass to a fail."
)

# pre-fill with the committed vendor-approval example (TTEC-DEMO-001).
left, right = st.columns(2)

with left:
    st.subheader("trace (what the agent did)")
    out_text = st.text_area(
        "output",
        value="Northwind Parts passed risk review under the approved vendors policy.",
        height=90,
        help="the agent's final answer text. checks read this.",
    )
    cite_span = st.text_input(
        "citation span",
        value="approved vendors policy",
        help="text of one citation span attached to the answer.",
    )
    tool_name = st.text_input(
        "tool call name",
        value="risk_lookup",
        help="name of one tool the agent called.",
    )

with right:
    st.subheader("checks (what the eval requires)")
    chk_present = st.text_input(
        "text_present -- output must contain",
        value="passed risk review",
    )
    chk_absent = st.text_input(
        "text_absent -- output must NOT contain",
        value="blocked vendor",
    )
    chk_cite = st.text_input(
        "citation_span_present -- a span must contain",
        value="approved vendors",
    )
    chk_tool = st.text_input(
        "tool_call_allowed -- agent must have called",
        value="risk_lookup",
    )
    chk_refusal = st.selectbox(
        "refusal_required",
        options=[False, True],
        index=0,
        help="true = the answer must read as a refusal; false = it must not.",
    )

# build a canonical trace from the editable inputs.
live_trace = {
    "trace_id": "user-edited",
    "framework": "langgraph",
    "input": "user-provided trace",
    "output": out_text,
    "citations": [{"source_id": "user", "span": cite_span}] if cite_span else [],
    "tool_calls": [{"name": tool_name}] if tool_name else [],
}

# build the check specs from the editable inputs (skip blanks where it makes sense).
live_checks = []
if chk_present:
    live_checks.append({"type": "text_present", "value": chk_present})
if chk_absent:
    live_checks.append({"type": "text_absent", "value": chk_absent})
if chk_cite:
    live_checks.append({"type": "citation_span_present", "value": chk_cite})
if chk_tool:
    live_checks.append({"type": "tool_call_allowed", "value": chk_tool})
live_checks.append({"type": "refusal_required", "value": chk_refusal})

# call the REAL engine, one check at a time.
results = [run_check(check, live_trace) for check in live_checks]
n_pass = sum(1 for r in results if r["status"] == "passed")
n_total = len(results)
case_passed = n_pass == n_total

m1, m2 = st.columns(2)
m1.metric("checks passing", f"{n_pass}/{n_total}")
m2.metric("case verdict", "PASS" if case_passed else "FAIL")

if case_passed:
    st.success(f"all {n_total} checks pass -- this trace would be green in the report.")
else:
    st.error(f"{n_total - n_pass} of {n_total} checks fail -- this case would be ranked failing-first.")

st.dataframe(
    [
        {
            "check": c["type"],
            "expects": c.get("value"),
            "status": r["status"],
            "why": r["message"],
        }
        for c, r in zip(live_checks, results)
    ],
    use_container_width=True,
    hide_index=True,
)
st.caption(
    "engine: `trace_to_eval_cli.runner.run_check`. clear the text_present field to "
    '"blocked vendor" or empty the tool name to watch a green check turn red live.'
)
