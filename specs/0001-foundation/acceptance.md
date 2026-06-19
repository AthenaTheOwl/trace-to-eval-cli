# Acceptance — 0001-foundation (trace-to-eval-cli)

v0 is done when the following commands all succeed on a clean clone.

## Commands

```powershell
uv sync
uv run trace-to-eval ingest langgraph examples/traces/langgraph/sample.jsonl --out examples/traces/canonical/sample.json
uv run trace-to-eval validate eval examples/eval_cases.yaml
uv run trace-to-eval validate trace examples/traces/canonical/sample.json
uv run trace-to-eval run examples/eval_cases.yaml --traces examples/traces/canonical --out reports/run.json
uv run trace-to-eval regress --baseline reports/baseline.json --current reports/run.json
uv run pytest
uv run python scripts/validate_schemas.py
uv run python scripts/voice_lint.py
uv run python scripts/dogfood.py
```

## Gates that must pass

- All tests pass under `pytest`.
- `validate_schemas.py` exits 0 against every JSON under `schemas/`,
  `examples/traces/canonical/`, and `reports/`.
- `voice_lint.py` exits 0 against every markdown under `docs/`.
- `dogfood.py` exits 0: the CLI runs end-to-end on the canonical
  fixture and the produced report matches the checked-in baseline.
- `trace-to-eval regress` exits 0 when baseline equals current and
  non-zero when a previously-passing case fails.

## Artifacts produced

- `schemas/trace.schema.json`, `schemas/eval-case.schema.json`,
  `schemas/run-report.schema.json` are present, valid JSON Schema
  2020-12, and self-test under `validate_schemas.py`.
- `reports/run.json` validates against the run-report schema.
- `reports/run.md` is human-readable and lists per-case status.
- `decisions/DEC-TTEC-001-trace-schema.md` is present and linked from
  the README.

## What v0 explicitly does not promise

- Adapters for frameworks other than LangGraph, CrewAI, Bedrock Agents.
- LLM-judge scoring.
- A hosted service.
- Trace storage. The user supplies the file path.
