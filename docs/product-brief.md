# Product Brief

## Product

Trace To Eval CLI is a local command-line repo for turning agent traces into
repeatable deterministic eval reports.

## First user action

`first_user_action: python -m trace_to_eval_cli validate`

That command succeeds with no flags. It validates the checked-in smoke eval case,
the canonical trace fixture, and the checked-in report artifact.

## User

- A builder with agent logs on disk who needs a repeatable pass or fail report.
- A team comparing framework traces without changing the framework runtime.
- A maintainer who wants a small fixture report in git before adding larger runs.

## v0.1 promise

- Define the trace, eval-case, and report shapes.
- Run deterministic checks against local traces.
- Keep the default path small enough to inspect by eye.
- Emit JSON and markdown reports that can be reviewed in a pull request.

## v0.1 non-goals

- Hosted storage.
- Network calls.
- Default LLM-judge scoring.
- Framework runtime patches.

