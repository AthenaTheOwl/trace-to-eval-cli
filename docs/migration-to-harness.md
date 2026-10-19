# Move new regression work to trace-to-eval-harness

This repository remains archived. Keep old traces and reports as historical
evidence and use `trace-to-eval-harness` for new regression work. Both projects
install a command named `trace-to-eval`, so prefer their explicit Python module
names or separate environments while migrating.

| Archived shape | Successor review action |
|---|---|
| `text_present` | Translate to `contains_required_text` with `case_insensitive: false`; the archived check is case-sensitive and the successor's default is not |
| `text_absent` | Translate to `does_not_contain_text` with `case_insensitive: false`, for the same reason |
| `citation_span_present` | The archived check reads only `citations[].span`; the successor also searches other citation text keys and `spans`. Preserve the source span and verify the successor trace shape |
| `tool_call_allowed` | Same name, different rule. The archived check passes only when the named tool was called; the successor's `allowed_tools` fails on any call outside the set and passes when no tool ran. The successor has no "this tool must run" check, so do not translate one-to-one; record the requirement as an open gap |
| `refusal_required` | The archived check takes `value: true` or `false` and matches `cannot comply`, `I can't`, `I cannot`, `unable to`. The successor always requires a refusal and has a different default marker list. For `true`, set `markers` to the archived terms; for `false`, use `does_not_contain_text` with those terms as `values` |
| `framework` and adapter metadata | Retain originals as provenance; do not assume every named adapter exists |

The archived trace schema's `spans` are offset records. The successor accepts
different span payloads, so do not blindly copy those arrays. Read both checked-in
schemas and normalize a trace into a new file, preserving its original beside it.
The archived schema names CrewAI and Bedrock but does not supply those ingest
adapters; migration must not promote a schema label into a working integration.

For each old failure, create one reviewed successor case and one clean control.
Run both against fixed saved traces, compare the named failed checks, and explain
any changed verdict. A clean control catches translations that fail every input.
Keep the baseline report, translated case, normalized trace, schema versions and
command output together. Preserve missing evidence as missing.

The successor's human-review boundary for generated cases remains in force.
This document is a manual compatibility map, not an automatic converter or a
new release of the archived CLI. It applies the version-and-evidence discipline
in [AI Product Team's change workflow](https://github.com/3orionkings/ai-product-team/blob/main/workflows/process-change.md).
