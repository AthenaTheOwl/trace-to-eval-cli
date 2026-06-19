# AGENTS.md — trace-to-eval-cli

Operating contract for AI agents (Claude, Codex, Cursor) working in
this repo. The conventions match the AthenaTheOwl portfolio so an
agent already trained on `trace-to-eval-harness` or
`supplier-risk-rag-agent` recognizes the shape.

## What this repo is

A public CLI plus schema plus adapter set. The product is the
trace format and the deterministic eval runner, not a hosted service.
Adapters target the agent frameworks the portfolio actually runs on.
Eval cases are YAML; reports are JSON plus markdown.

## Voice constraints

- No marketing words. The banned set will live in
  `scripts/voice_lint.py::BANNED_FAIL` once the lint script lands in
  spec 0002. Examples that always fail: leverage, demonstrate, seamless,
  cutting-edge, best-in-class, synergy.
- No antithetical reversals as a structural device.
- Plain assertions. Schemas plus tests are the moat; the prose is
  scaffolding.

## Gates

Will land in spec `0002-cli-and-adapters`. The intended chain:

- `voice_lint` on every checked-in markdown.
- `validate_schemas` on every example trace, eval case, and report.
- `pytest` against the adapter and check matrix.
- `dogfood` step that runs the CLI against the portfolio's own
  fixture trace bundle and asserts the report matches the baseline.

## Out of scope

- A hosted service. The CLI runs locally; trace storage is the user's
  problem.
- LLM-judge scoring as a default. v0 is deterministic checks. An
  LLM-judge plugin can land later under its own spec.
- A web UI. Reports are markdown plus JSON.
- Framework-internal patches. Adapters read whatever a framework
  already emits; no monkey-patching.
