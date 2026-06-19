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

v0 scaffold. No implementation yet. The harness prototype lives in the
sibling `trace-to-eval-harness` repo; this repo is the public CLI
productization. The first PR after the scaffold lands the trace schema
and the LangGraph adapter; see `docs/first-pr.md`.

## How to run

Placeholder. Run commands will land in spec `0002-cli-and-adapters`.
The shape will be:

```powershell
uv sync
uv run trace-to-eval ingest langgraph traces/raw/my_run.jsonl --out cases/my_run.yaml
uv run trace-to-eval validate cases/my_run.yaml
uv run trace-to-eval run cases/my_run.yaml --traces traces/raw --out reports/run.json
uv run trace-to-eval regress --baseline reports/baseline.json --current reports/run.json
```

## Layout

```
trace-to-eval-cli/
  AGENTS.md
  LICENSE
  README.md
  specs/
    0001-foundation/
      requirements.md
      design.md
      tasks.md
      acceptance.md
  docs/
    first-pr.md
  src/
    cli/                # main.py with subcommands
    ingest/             # langgraph_adapter, crewai_adapter, bedrock_adapter
    eval/               # regression_runner, deterministic checks
    schemas/            # trace.schema.json, eval-case.schema.json
  examples/             # tiny worked traces per adapter
  tests/                # pytest cases per adapter and per check
  decisions/            # DEC-TTEC-* architectural choices
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
