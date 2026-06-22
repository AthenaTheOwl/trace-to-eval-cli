from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .io import CliDataError


def load_canonical_trace(path: Path) -> dict[str, Any]:
    try:
        trace = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CliDataError(f"trace file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CliDataError(f"invalid trace JSON in {path}: {exc.msg}") from exc

    validate_trace_shape(trace, path)
    return trace


def ingest_langgraph_jsonl(path: Path) -> dict[str, Any]:
    trace_id = ""
    trace_input = ""
    trace_output = ""
    citations: list[dict[str, str]] = []
    tool_calls: list[dict[str, Any]] = []

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise CliDataError(f"LangGraph trace file not found: {path}") from exc

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise CliDataError(f"invalid JSONL at {path}:{line_number}: {exc.msg}") from exc

        trace_id = trace_id or str(event.get("run_id", ""))
        event_name = event.get("event")
        data = event.get("data", {})
        if not isinstance(data, dict):
            raise CliDataError(f"event data must be an object at {path}:{line_number}")

        if event_name == "on_chain_start":
            trace_input = str(data.get("input", ""))
        elif event_name == "on_tool_end":
            tool_calls.append(
                {
                    "name": str(event.get("name", "")),
                    "arguments": data.get("arguments", {}),
                    "output": str(data.get("output", "")),
                }
            )
        elif event_name == "on_llm_end":
            trace_output = str(data.get("output", ""))
            raw_citations = data.get("citations", [])
            if isinstance(raw_citations, list):
                citations = [
                    {"source_id": str(item.get("source_id", "")), "span": str(item.get("span", ""))}
                    for item in raw_citations
                    if isinstance(item, dict)
                ]

    trace = {
        "trace_id": trace_id,
        "framework": "langgraph",
        "input": trace_input,
        "output": trace_output,
        "citations": citations,
        "spans": [{"name": "answer", "start": 0, "end": len(trace_output)}],
        "tool_calls": tool_calls,
        "expected_behavior": "Return a deterministic approval answer with one policy citation.",
        "failure_tags": [],
    }
    validate_trace_shape(trace, path)
    return trace


def validate_trace_shape(trace: dict[str, Any], path: Path | None = None) -> None:
    source = f" in {path}" if path else ""
    for field in ("trace_id", "framework", "input", "output"):
        if not isinstance(trace.get(field), str) or not trace[field]:
            raise CliDataError(f"trace{source} missing required string field: {field}")
    if trace["framework"] not in {"langgraph", "crewai", "bedrock", "passthrough"}:
        raise CliDataError(f"trace{source} has unsupported framework: {trace['framework']}")

