# Spec 0002 acceptance

The v0.1 release is accepted when:

- `python -m trace_to_eval_cli validate` exits 0 with no flags.
- `python -m pytest -q` passes.
- `reports/ttec_v0_1_smoke.jsonl` exists beside the JSON and markdown report.
