# Requirements — 0001-foundation (trace-to-eval-cli)

Brand prefix: `TTEC`.

## Scope

The foundation spec names the trace schema, the eval-case schema, the
CLI surface, the first three adapters, and the eval-check set that v0
must support.

## Requirements

- R-TTEC-001: The repo publishes `schemas/trace.schema.json` with a
  stable `$id` of `https://trace-to-eval.dev/schemas/v1/trace.schema.json`.
  The schema's required fields are `trace_id`, `framework`, `input`,
  `output`. Optional: `citations`, `spans`, `tool_calls`,
  `expected_behavior`, `failure_tags`.
- R-TTEC-002: The repo publishes `schemas/eval-case.schema.json`.
  Required fields per case: `id`, `suite`, `trace_id`, `checks`. Each
  check has a `type` and a `value` or `pattern`.
- R-TTEC-003: The CLI exposes the subcommands `ingest`, `validate`,
  `run`, `regress`. Each subcommand prints help under `-h` and exits
  non-zero on any failure.
- R-TTEC-004: v0 ships three ingest adapters: LangGraph (`langgraph`),
  CrewAI (`crewai`), Bedrock Agents (`bedrock`). Adding a new adapter
  is one new file under `src/ingest/` plus one fixture under
  `examples/traces/`.
- R-TTEC-005: v0 ships at least five deterministic check types:
  `text_present`, `text_absent`, `citation_span_present`,
  `tool_call_allowed`, `refusal_required`.
- R-TTEC-006: `trace-to-eval run` writes both `reports/<name>.json`
  and `reports/<name>.md`. The JSON validates against
  `schemas/run-report.schema.json`.
- R-TTEC-007: `trace-to-eval regress --baseline X --current Y` exits
  non-zero if any check that passed in `X` fails in `Y`. New failures
  block; new passes are allowed.
- R-TTEC-008: Every example trace under `examples/traces/` validates
  against the trace schema. CI fails on any drift.
- R-TTEC-009: No network call from any code path under `src/`. Adapters
  read from disk only.
- R-TTEC-010: The CLI does not require an LLM API key for any v0
  subcommand. Determinism is enforced by the check set.
- R-TTEC-011: A `voice_lint` pass runs against every markdown under
  `docs/` and `reports/`.
- R-TTEC-012: Decision records live under `decisions/DEC-TTEC-NNN.md`.
  The first is `DEC-TTEC-001-trace-schema.md`.
