# Tasks — 0001-foundation (trace-to-eval-cli)

Ordered for the first two to three PRs after this scaffold lands.

## PR 1 — schemas and the LangGraph adapter

- [ ] Add `pyproject.toml` with `pydantic`, `jsonschema`, `typer`, `pyyaml`, `pytest`, `ruff`.
- [ ] Add `schemas/trace.schema.json` with the v0 trace shape.
- [ ] Add `schemas/eval-case.schema.json`.
- [ ] Add `schemas/run-report.schema.json`.
- [ ] Add `src/trace_to_eval/ingest/base.py` declaring the `Adapter` protocol.
- [ ] Add `src/trace_to_eval/ingest/langgraph_adapter.py`.
- [ ] Add `examples/traces/langgraph/sample.jsonl` and the normalized `examples/traces/canonical/sample.json`.
- [ ] Add `tests/test_langgraph_adapter.py` covering happy-path and one missing-field case.
- [ ] Add `decisions/DEC-TTEC-001-trace-schema.md`.

## PR 2 — eval runner and three check types

- [ ] Add `src/trace_to_eval/eval/checks/text_present.py`.
- [ ] Add `src/trace_to_eval/eval/checks/text_absent.py`.
- [ ] Add `src/trace_to_eval/eval/checks/citation_span_present.py`.
- [ ] Add `src/trace_to_eval/eval/runner.py`.
- [ ] Add `examples/eval_cases.yaml`.
- [ ] Add `tests/test_runner.py` exercising the three checks.
- [ ] Add `src/trace_to_eval/cli/main.py` plus `cli/run.py`, `cli/validate.py`.
- [ ] Add `scripts/validate_schemas.py` and wire as gate.

## PR 3 — adapters for CrewAI and Bedrock plus regression

- [ ] Add `src/trace_to_eval/ingest/crewai_adapter.py`.
- [ ] Add `src/trace_to_eval/ingest/bedrock_adapter.py`.
- [ ] Add fixtures under `examples/traces/crewai/` and `examples/traces/bedrock/`.
- [ ] Add `src/trace_to_eval/eval/regression.py` plus `cli/regress.py`.
- [ ] Add `src/trace_to_eval/eval/checks/tool_call_allowed.py`.
- [ ] Add `src/trace_to_eval/eval/checks/refusal_required.py`.
- [ ] Add `scripts/voice_lint.py` and wire as gate.
- [ ] Add `scripts/dogfood.py` that runs the CLI end-to-end on the canonical fixture and diffs the report.
