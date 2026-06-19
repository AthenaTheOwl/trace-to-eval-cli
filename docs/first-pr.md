# First PR — trace-to-eval-cli

The literal first PR after the scaffold. Narrow scope so review is
fast and the schema-validation gate is real on day one.

## Title

`feat(TTEC): trace schema plus LangGraph adapter (PR 1)`

## Goal

Land the three JSON Schemas that constrain the rest of the project,
plus the LangGraph adapter as the first proof that the trace shape
covers a real-world framework output.

## Files added

- `pyproject.toml` — deps: `pydantic`, `jsonschema`, `typer`,
  `pyyaml`, `pytest`, `ruff`.
- `src/trace_to_eval/__init__.py` — exposes `__version__`.
- `src/trace_to_eval/ingest/__init__.py`
- `src/trace_to_eval/ingest/base.py` — declares the `Adapter`
  protocol; pure type definitions, no runtime cost.
- `src/trace_to_eval/ingest/langgraph_adapter.py` — reads a LangGraph
  JSONL event stream, joins `on_chain_start`/`on_tool_end`/`on_llm_end`
  events into one canonical `Trace`.
- `schemas/trace.schema.json` — v0 trace shape.
- `schemas/eval-case.schema.json` — v0 case shape.
- `schemas/run-report.schema.json` — v0 report shape.
- `examples/traces/langgraph/sample.jsonl` — small, hand-curated
  LangGraph event stream.
- `examples/traces/canonical/sample.json` — the expected normalized
  output of running the adapter on the fixture.
- `tests/test_langgraph_adapter.py` — runs the adapter, diffs against
  the canonical sample, covers one missing-field path.
- `tests/test_schemas_self.py` — validates each schema against
  JSON Schema 2020-12.
- `scripts/validate_schemas.py` — walks `schemas/` plus
  `examples/traces/canonical/` and exits 1 on any mismatch.
- `decisions/DEC-TTEC-001-trace-schema.md` — names the v0 trace
  shape and the reasons for each field choice.

## Files not in this PR

- Eval runner. PR 2.
- CrewAI and Bedrock adapters. PR 3.
- Regression comparator. PR 3.
- Any CI workflow.

## Verification

Reviewer runs:

```powershell
uv sync
uv run pytest
uv run python scripts/validate_schemas.py
```

Expected: all tests pass; `validate_schemas.py` exits 0.

## Review checklist

- [ ] Every schema declares `$id` and `$schema`.
- [ ] The LangGraph fixture is small enough to read by eye.
- [ ] The adapter does not call out over the network.
- [ ] The decision record names the field set and the alternatives
      that were rejected.
- [ ] No marketing words in any added markdown.

## After merge

PR 2 lands the runner plus three check types and the `run` / `validate`
CLI subcommands. PR 3 adds the remaining two adapters, the regression
comparator, and the dogfood gate.
