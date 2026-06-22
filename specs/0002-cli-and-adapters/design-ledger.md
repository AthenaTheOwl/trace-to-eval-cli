# Design Ledger - 0002 CLI And Adapters

## Scope

Spec 0002 turns the foundation scaffold into a runnable v0.1 data-report repo.

## Ledger

| ID | Decision | Status | Evidence |
| --- | --- | --- | --- |
| D-0002-001 | Use `argparse` for the v0 CLI. | accepted | `trace_to_eval_cli/cli.py` has no runtime dependency. |
| D-0002-002 | Keep `validate` runnable with no flags. | accepted | `python -m trace_to_eval_cli validate` uses the smoke fixture paths. |
| D-0002-003 | Keep eval cases as JSON-compatible YAML for v0.1. | accepted | The loader works without PyYAML but uses it when present. |
| D-0002-004 | Make the checked-in smoke report deterministic. | accepted | The default report uses a fixed run id and timestamp. |
| D-0002-005 | Treat adapters as disk readers only. | accepted | The LangGraph adapter reads JSONL and performs no network calls. |

## Checks in v0.1

- `text_present`
- `text_absent`
- `citation_span_present`
- `tool_call_allowed`
- `refusal_required`

## Open items

- Add CrewAI and Bedrock fixtures.
- Add a full JSON Schema validator gate after dependency policy is approved.
- Add a larger dogfood bundle after the smoke path is stable.

