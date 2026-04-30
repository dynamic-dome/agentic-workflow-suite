#!/usr/bin/env python3
"""
raw-write-guard hook — warns when a write attempt targets wiki/raw/.

Mode: warn-only (V2 read-only checker per hooks-readonly.md).
Event: PreToolUse with tool in {Write, Edit, NotebookEdit, mcp__wiki__wiki_write, mcp__wiki__wiki_append_section}.

Exit codes:
  0 — allow, no warning
  0 + stderr — allow but show warning
  We never use exit 2 (block) in V2.

Audit log: ~/.claude/logs/raw-write-guard.ndjson
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


LOG_PATH = Path.home() / ".claude" / "logs" / "raw-write-guard.ndjson"


def main() -> int:
    try:
        event = json.loads(sys.stdin.read())
    except Exception:
        return 0

    tool_input = event.get("tool_input") or {}
    target = tool_input.get("file_path") or tool_input.get("path") or ""
    target_norm = target.replace("\\", "/")

    if not target_norm:
        return 0

    if "wiki/raw/" in target_norm:
        log_entry(event, target_norm, "warn")
        sys.stderr.write(
            f"raw-write-guard: write attempt on raw inbox: {target}. "
            f"Raw files are read-only. If intentional, confirm in chat.\n"
        )
        return 0

    log_entry(event, target_norm, "allow")
    return 0


def log_entry(event: dict, target: str, decision: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": event.get("tool_name", "unknown"),
        "target": target,
        "decision": decision,
    }
    try:
        with LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
    except Exception:
        pass


if __name__ == "__main__":
    sys.exit(main())
