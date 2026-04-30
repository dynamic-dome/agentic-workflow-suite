#!/usr/bin/env python3
"""
private-export-gate hook — warns when a private source might be exported to NotebookLM/wiki/external.

Mode: warn-only.
Event: PreToolUse with tool in {mcp__notebooklm__nlm_add_source_url, mcp__notebooklm__nlm_add_source_text, WebFetch, mcp__wiki__wiki_write, mcp__wiki__wiki_append_section}.

Heuristic for 'private': source path contains any of:
  - 'diary/', 'private/', 'persoenlich/', 'personal/'
  - 'wiki/raw/' (raw inbox is private-by-default)
  - file extension matches /\.(md|txt)$/i AND parent dir mentions private

This hook does NOT inspect content — only path heuristics.

Audit log: ~/.claude/logs/private-export-gate.ndjson
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


LOG_PATH = Path.home() / ".claude" / "logs" / "private-export-gate.ndjson"

PRIVATE_MARKERS = (
    "diary/",
    "private/",
    "persoenlich/",
    "personal/",
    "wiki/raw/",
    "telegram-privat",
)

EXPORT_TOOLS = (
    "mcp__notebooklm__nlm_add_source_url",
    "mcp__notebooklm__nlm_add_source_text",
    "WebFetch",
    "mcp__wiki__wiki_write",
    "mcp__wiki__wiki_append_section",
)


def main() -> int:
    try:
        event = json.loads(sys.stdin.read())
    except Exception:
        return 0

    tool_name = event.get("tool_name", "")
    if tool_name not in EXPORT_TOOLS:
        return 0

    tool_input = event.get("tool_input") or {}
    candidates = []
    for key in ("file_path", "path", "url", "source_url", "source_text"):
        val = tool_input.get(key)
        if isinstance(val, str):
            candidates.append(val)

    haystack = " | ".join(candidates).lower().replace("\\", "/")

    if any(marker in haystack for marker in PRIVATE_MARKERS):
        log_entry(tool_name, haystack, "warn")
        sys.stderr.write(
            f"private-export-gate: tool '{tool_name}' may export a private source. "
            f"Confirm explicit export intent before proceeding.\n"
        )
        return 0

    log_entry(tool_name, haystack, "allow")
    return 0


def log_entry(tool: str, haystack: str, decision: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": tool,
        "haystack_preview": haystack[:200],
        "decision": decision,
    }
    try:
        with LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
    except Exception:
        pass


if __name__ == "__main__":
    sys.exit(main())
