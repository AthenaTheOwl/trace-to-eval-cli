# Trace To Eval CLI Status

## Current state

- Archived 2026-07-01. The adapter layer this repo was building folds into trace-to-eval-harness, so work continues there instead of here.
- v0.1 ships a local Python package with `python -m trace_to_eval_cli validate` as the first user action.
- The default validation uses the checked-in smoke eval case, canonical trace, and report artifact.
- The CLI can ingest a small LangGraph JSONL fixture, run deterministic checks, validate fixtures, and compare reports.
- JSON schemas, a product brief, a system map, a spec 0002 design ledger, tests, and one smoke report artifact are checked in.

## Known limits

- YAML support is limited to JSON-compatible YAML unless PyYAML is installed in the caller's environment.
- The adapter surface covers the checked-in LangGraph fixture and a passthrough canonical trace path only.
- Report generation is deterministic for the smoke fixture and does not yet include wall-clock run metadata.
- The schema script performs structural checks without pulling a JSON Schema validator dependency at runtime.

## Next feature queue

- Add CrewAI and Bedrock fixture adapters with one canonical trace each.
- Replace the structural schema script with full JSON Schema 2020-12 validation after dependency policy is approved.
- Add a larger dogfood bundle drawn from the portfolio trace harness.
- Add regression examples where one prior pass becomes a current failure.

