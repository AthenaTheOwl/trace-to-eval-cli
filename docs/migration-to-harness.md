# Move new regression work to trace-to-eval-harness

This repository remains archived. Keep old traces and reports as historical
evidence and use `trace-to-eval-harness` for new regression work. Both projects
install a command named `trace-to-eval`, so prefer their explicit Python module
names or separate environments while migrating.

| Archived shape | Successor review action |
|---|---|
| `text_present` | Translate to `contains_required_text` and check exact semantics |
| `text_absent` | Translate to `does_not_contain_text` |
| `citation_span_present` | Preserve source span and verify the successor trace shape |
| `tool_call_allowed` | Preserve the allowed set and actual tool-call names |
| `refusal_required` | Inspect the successor's deterministic refusal rule |
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
