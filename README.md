# TraceToEval

Open-source CLI that takes any agent trace log and emits an evaluable
test suite with regression tracking. The productized form of the
`trace-to-eval-harness` prototype.

## What this is

Every agent framework ships traces in a different shape. LangGraph,
CrewAI, Bedrock Agents, OpenAI Agents SDK, Claude Code, custom Python
factories — none of them agree on a normalized format, and almost none
of them ship a path from "this trace is a failure" to "this failure
is a regression test that runs in CI."

TraceToEval is the lower layer that DreamReplay and the Notary Layer
both depend on. It defines a single trace schema, ships ingest adapters
for the common frameworks, and runs deterministic eval cases against
either fresh runs or historical traces.

Bucket: agent-ops. Category: agent-ops. Brand prefix: `TTEC`.

## Who this is for

- Individual builders running their own agent stacks.
- Eng teams on agent frameworks (LangGraph, CrewAI, Bedrock) who want
  a normalized trace surface across vendors.
- Researchers comparing agent behavior across frameworks.
- The author's own portfolio, dogfooded across every agent-shaped repo.

## Status


v0.1 shipped and runs end to end. The entry command `python -m trace_to_eval_cli validate` runs. See `specs/0002-design/` for the v0.1 scope and `STATUS.md` (where present) for the current state and next-feature queue.

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

Only the `langgraph` adapter exists today; `crewai` and `bedrock` are
accepted in the trace schema but have no ingest adapter yet.

## live demo

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

## Relationship to trace-to-eval-harness

`trace-to-eval-harness` is the internal prototype that runs across the
portfolio. This repo is the public CLI. Schemas and check semantics
will track between the two; the public repo carries the standards-track
work (RFC, spec, conformance suite) and the framework adapters.

## Compounds with

- DreamReplay consumes the trace format and emits weekly dream candidates.
- Notary Layer attaches receipts to traces emitted by this CLI.
- ProofGateRunner uses the eval-runner as one of its gates.
- Every agent-shaped repo in the portfolio is a dogfood adapter target.

## License

MIT. See [LICENSE](LICENSE).
