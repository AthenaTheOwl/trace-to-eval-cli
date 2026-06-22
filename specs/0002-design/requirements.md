# Spec 0002 requirements

## R-TTEC-002-001 - default validation

`python -m trace_to_eval_cli validate` must run with no flags and validate the
smoke eval case, canonical trace, and checked report artifact.

## R-TTEC-002-002 - deterministic report

The smoke report must be reproducible from checked-in fixtures and stored under
`reports/`.

## R-TTEC-002-003 - adapter boundary

Adapters read local trace files only. Network calls and live framework runtimes
are out of scope for v0.1.
