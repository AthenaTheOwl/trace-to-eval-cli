# System Map

## Data flow

1. A framework trace file is read from disk.
2. An adapter normalizes it into the canonical trace shape.
3. An eval case names a trace and a list of deterministic checks.
4. The runner evaluates each check and builds a report.
5. The CLI writes JSON and markdown report files.

## Modules

- `trace_to_eval_cli.cli`: argparse entry point and subcommands.
- `trace_to_eval_cli.adapters`: LangGraph fixture ingest and passthrough loading.
- `trace_to_eval_cli.runner`: check execution and report creation.
- `trace_to_eval_cli.io`: JSON and JSON-compatible YAML loading.
- `schemas`: JSON Schema documents for the three public data shapes.
- `examples`: smoke eval case and trace fixtures.
- `reports`: checked-in v0.1 report artifact.
- `scripts`: local gates for schema checks, voice checks, and dogfood.

## Default scenario

- Eval case: `examples/eval-cases/ttec_smoke.yaml`
- Trace: `examples/traces/canonical/ttec_smoke.json`
- Report: `reports/ttec_v0_1_smoke.json`

