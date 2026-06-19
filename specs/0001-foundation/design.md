# Design — 0001-foundation (trace-to-eval-cli)

## Shape

Three layers. Ingest adapters normalize framework-specific trace logs
into the canonical trace schema. The eval runner reads eval-case YAML
plus normalized traces and emits a run report. The regression
comparator reads two reports and prints a verdict.

## Layers

### Ingest (`src/ingest/`)

- `base.py` — declares the `Adapter` protocol: `load(path) -> Iterator[Trace]`.
- `langgraph_adapter.py` — parses LangGraph's JSONL event stream into
  the canonical trace shape. Handles `on_chain_start`, `on_tool_end`,
  `on_llm_end` events.
- `crewai_adapter.py` — parses CrewAI's task-output JSON dumps.
- `bedrock_adapter.py` — parses Bedrock Agents trace responses
  (the `trace` field on `InvokeAgent` streaming events).
- `passthrough.py` — for repos that already emit canonical traces.

### Eval (`src/eval/`)

- `runner.py` — loads cases, loads referenced traces, executes the
  check matrix, emits a `RunReport`.
- `checks/text_present.py`, `checks/text_absent.py`,
  `checks/citation_span_present.py`, `checks/tool_call_allowed.py`,
  `checks/refusal_required.py` — one file per check type. New check
  types are registered in `checks/__init__.py`.
- `regression.py` — pure function that takes two `RunReport`s and
  emits a `RegressionVerdict`.

### CLI (`src/cli/`)

- `main.py` — top-level entry point. Uses `typer` or `argparse`;
  decision recorded in `DEC-TTEC-002-cli-framework.md`.
- `ingest.py`, `validate.py`, `run.py`, `regress.py` — subcommand
  implementations.

## Data shapes

```
trace.json:
  trace_id: str
  framework: "langgraph" | "crewai" | "bedrock" | "passthrough"
  input: str
  output: str
  citations?: list[Citation]
  spans?: list[Span]
  tool_calls?: list[ToolCall]
  failure_tags?: list[str]

eval-case.yaml:
  cases:
    - id: str
      suite: str
      trace_id: str
      trace_file: str        # path relative to --traces dir
      checks:
        - type: text_present
          value: "raised the filing count to 42"

run-report.json:
  run_id: str
  generated_at: iso8601
  case_results:
    - case_id: str
      suite: str
      status: passed | failed | skipped
      check_results: [...]
```

## Non-goals

- LLM-judge scoring. v0 is deterministic.
- Trace storage. The CLI reads from disk; storage is the user's.
- A normalized schema for *framework* internals. Only the trace shape.
