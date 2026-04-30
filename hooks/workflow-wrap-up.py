#!/usr/bin/env python3
"""
workflow-wrap-up hook — at session Stop, reminds the agent to capture artifacts, tests, open risks, next step.

Mode: warn-only (informational reminder).
Event: Stop.

The hook does NOT block stop. It only emits a reminder to stderr so the agent
can decide whether to do a final wrap-up step.

Audit log: ~/.claude/logs/workflow-wrap-up.ndjson
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


LOG_PATH = Path.home() / ".claude" / "logs" / "workflow-wrap-up.ndjson"


def main() -> int:
    try:
        event = json.loads(sys.stdin.read())
    except Exception:
        return 0

    log_entry(event)
    sys.stderr.write(
        "workflow-wrap-up: session ending. Did you capture: "
        "(1) artifacts/files changed, (2) tests run + result, "
        "(3) open risks, (4) next concrete step? "
        "If yes, ignore. If no, run /agentic-os:wrap-up or write a session note.\n"
    )
    return 0


def log_entry(event: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "stop",
    }
    try:
        with LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
    except Exception:
        pass


if __name__ == "__main__":
    sys.exit(main())
