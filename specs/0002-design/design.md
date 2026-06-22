# Spec 0002 design

The CLI reads a trace fixture, normalizes it to the canonical trace shape, runs
deterministic checks from the eval case, and writes a report. The default
validation path is intentionally tiny so a reviewer can inspect every fixture.
