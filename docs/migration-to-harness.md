# Move new regression work to trace-to-eval-harness

This repository remains archived. Keep old traces and reports as historical
evidence and use `trace-to-eval-harness` for new regression work. The successor
installs the `trace-to-eval` command. This archived CLI installs
`trace-to-eval-legacy` (it was also named `trace-to-eval` before 2026-10-19, so
installing both replaced one script with the other). Both can now share one
environment while migrating:

```bash
trace-to-eval-legacy ingest langgraph old.jsonl --out normalized.json  # archived CLI
trace-to-eval validate eval translated_case.yaml                        # successor
```

The module forms `python -m trace_to_eval_cli` and `python -m trace_to_eval`
work as well.

Two archived commands have no successor counterpart. There is no `regress`: run
the successor's `run --fail-on-failure` and compare reports by hand, as below.
There is no LangGraph JSONL ingest: run the archived
`trace-to-eval-legacy ingest langgraph` first, then normalize its output.
The successor's `ingest` shares the name but takes a trace JSON that is already in
its shape and writes a draft YAML eval case, not a normalized trace.

| Archived shape | Successor review action |
|---|---|
| `text_present` | Translate to `contains_required_text` with `case_insensitive: false`; the archived check is case-sensitive and the successor's default is not |
| `text_absent` | Translate to `does_not_contain_text` with `case_insensitive: false`, for the same reason |
| `citation_span_present` | Keep `citation_span_present` with `case_insensitive: false`, for the same reason. The archived check reads only `citations[].span` and matches one span at a time; the successor also searches other citation text keys and `spans`, joined with newlines, so a value can match across two citations. Preserve the source span and verify the successor trace shape. An archived check with an empty or missing `value` (and no `pattern`) means "at least one citation exists" and fails on a trace with no citations; the successor passes an empty `value` on every trace, and `validate eval` accepts it. The successor has no equivalent, so record it as an open gap, as for `tool_call_allowed` |
| `tool_call_allowed` | Same name, different rule. The archived check passes only when the named tool was called; the successor's `allowed_tools` fails on any call outside the set and passes when no tool ran. The successor has no "this tool must run" check, so do not translate one-to-one; record the requirement as an open gap |
| `refusal_required` | The archived check reads the truthiness of `value`: a missing value, an empty string or `false` means the output must not refuse; `true` or any non-empty string, including `"false"`, means it must. It matches `cannot comply`, `I can't`, `I cannot`, `unable to`, ignoring case. The successor always requires a refusal and has a different default marker list. When the archived check requires a refusal, set `markers` to the archived terms; otherwise use `does_not_contain_text` with those terms as `values` |
| `framework` and adapter metadata | Retain originals as provenance; do not assume every named adapter exists |

The archived runner reads `pattern` when a check has no `value`. Move it to
`value` before translating: the successor ignores `pattern`, and a text or
citation check left with no `value` or `values` passes on any output. The
successor's `run` does not schema-check case files, so run its `validate eval`
on each translated file; that rejects a leftover `pattern`.

Archived traces that carry a non-empty `expected_behavior` do not load in the
successor as they stand. The archived `expected_behavior` is a string, and every
checked-in archived trace has one; the successor requires an object and rejects
the trace, so drop it or wrap it (for example as `{"description": ...}`) in the
normalized copy. Traces produced by the archived `ingest langgraph` all carry the
same fixed placeholder string, which says nothing about that run, so drop it; wrap
it only when a person wrote it for that trace. Archived `failure_tags`
and case `suite` values are free-form, while the successor's schemas accept only
fixed lists (`no_citation`, `guardrail` and `vendor-approval` are not on them), so
map them. The archived offset `spans` load unchanged but supply no citation text.
Read both checked-in schemas and normalize a trace into a new file, preserving its
original beside it.
The archived schema names CrewAI and Bedrock but does not supply those ingest
adapters; migration must not promote a schema label into a working integration.

For each old failure, create one reviewed successor case and one clean control.
Run both against fixed saved traces, compare the named failed checks, and explain
any changed verdict. A clean control catches translations that fail every input.
Keep the baseline report, translated case, normalized trace, the schema files used
(by commit hash or checksum; the two repos reuse the same `$id` for different
schemas, and the archived ones carry no version) and command output together. Preserve missing evidence as missing.

The successor's human-review boundary for generated cases remains in force.
This document is a manual compatibility map, not an automatic converter or a
new release of the archived CLI.
