# trace-to-eval-cli

Status: archived 2026-07-01. Successor is trace-to-eval-harness, which folds in the adapter layer this repo was building.

A guardrail case fails. The refusal that was required never came. Without a record, that failure is a story someone tells in a standup; with one, it is a test that runs in CI and stays failed until the refusal returns. This CLI does the conversion.

## What it does

Every agent framework writes its traces in a different shape. LangGraph, CrewAI, Bedrock Agents, the OpenAI Agents SDK, Claude Code, a hand-rolled Python factory — none of them agree on a normalized format, and almost none of them carry a path from "this trace is a failure" to "this failure is a regression test." The failure stays anecdotal. It gets fixed, or it gets forgotten, and either way nobody can prove it later.

This tool defines one trace schema, normalizes raw traces into it, and runs deterministic eval cases against either fresh runs or historical traces. A case that passed in the baseline and fails now exits non-zero. The checks are the point; the framework adapters are deliberately thin, and today only one of them is real — `langgraph`. `crewai` and `bedrock` are accepted in the schema and have no ingest adapter yet.

## Try it

One command, no setup, no keys. It reads the committed demo report and prints the ranked view:

```bash
python -m trace_to_eval_cli show
```

```
trace eval report: ttec-v0.1-demo  (generated 2026-06-22T00:00:00Z)
  3 case(s): 2 passed, 1 failed, 0 skipped  --  66.7% pass rate

   #  case           suite            status   checks
  ---------------------------------------------------
   1  TTEC-DEMO-003  guardrail        failed   0/3 ok, 3 failing
   2  TTEC-DEMO-001  vendor-approval  passed   5/5 ok
   3  TTEC-DEMO-002  vendor-block     passed   3/3 ok

finding: 1 of 3 case(s) failing. worst: TTEC-DEMO-003 (guardrail) - refusal_required: refusal expectation was not met.
```

The failing case is named, with the check that broke it. That line is what a regression run hands you instead of a shrug.

## Live demo

A read-only streamlit page renders the same ranked eval report the `show`
verb prints. It reads the committed `reports/ttec_v0_1_demo.json` directly —
no network, no keys.

Run it locally:

```bash
uv run --with streamlit streamlit run streamlit_app.py
```

Deploy on Streamlit Community Cloud: New app -> repo
`AthenaTheOwl/trace-to-eval-cli`, branch `main`, main file `streamlit_app.py`.

<!-- live-url: https://__________.streamlit.app -->

## How to run

The CLI is installed as `trace-to-eval` (or run the module with
`python -m trace_to_eval_cli`). All commands are offline and deterministic.

```bash
uv sync

# print a ranked, readable view of the committed demo report (no args)
python -m trace_to_eval_cli show

# validate that the committed report matches what the checks compute now
python -m trace_to_eval_cli validate

# run a case file against a traces dir and write json + markdown reports
python -m trace_to_eval_cli run \
  --case examples/eval-cases/ttec_demo.json \
  --traces examples/traces/canonical \
  --out reports/run.json --md-out reports/run.md

# normalize a raw langgraph jsonl trace into the canonical shape
python -m trace_to_eval_cli ingest langgraph examples/traces/langgraph/sample.jsonl \
  --out examples/traces/canonical/sample.json

# fail if a case that passed in the baseline is failing now
python -m trace_to_eval_cli regress \
  --baseline reports/ttec_v0_1_smoke.json --current reports/run.json
```

## How it connects

This CLI is the floor the trace-shaped repos stand on — it sets the schema everything else reads and writes.

- [dream-replay-cli](https://github.com/AthenaTheOwl/dream-replay-cli) — consumes the trace format and surfaces weekly dream candidates from it.
- [agent-notary-layer](https://github.com/AthenaTheOwl/agent-notary-layer) — attaches receipts to the traces this CLI emits.
- [proof-gate-runner](https://github.com/AthenaTheOwl/proof-gate-runner) — runs the eval-runner here as one of its gates.
- [trace-ledger-spec](https://github.com/AthenaTheOwl/trace-ledger-spec) — the standards-track schema work the adapters track against.

[trace-to-eval-harness](https://github.com/AthenaTheOwl/trace-to-eval-harness) is the internal prototype that runs across the portfolio; this is its public CLI. Schemas and check semantics track between the two.

## Layout

```
trace-to-eval-cli/
  AGENTS.md
  LICENSE
  README.md
  streamlit_app.py        # live-demo page (reads reports/ttec_v0_1_demo.json)
  requirements.txt        # streamlit + this package, for Streamlit Cloud
  trace_to_eval_cli/
    cli.py                # subcommands: show / validate / run / ingest / regress
    adapters.py           # langgraph jsonl -> canonical trace
    runner.py             # build_report, summarize_report, compare_reports
    scoring.py            # status rollup
  schemas/                # trace.schema.json, eval-case.schema.json, run-report.schema.json
  examples/
    eval-cases/           # ttec_smoke.yaml, ttec_demo.json
    traces/canonical/     # canonical trace fixtures
    traces/langgraph/     # raw langgraph jsonl sample
  reports/                # committed json + md reports
  tests/                  # pytest cases per command and per check
  specs/                  # 0001-foundation, 0002-design
```

## License

MIT. See [LICENSE](LICENSE).
