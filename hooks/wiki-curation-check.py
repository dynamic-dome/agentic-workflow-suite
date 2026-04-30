#!/usr/bin/env python3
"""
wiki-curation-check hook — warns if a fresh wiki page lacks frontmatter, index link, or log entry.

Mode: warn-only.
Event: PostToolUse with tool in {mcp__wiki__wiki_write, mcp__wiki__wiki_append_section, Write, Edit}.

Findings (any of which produce a warning):
  - no YAML frontmatter
  - frontmatter without 'type' field
  - page basename not in wiki/index.md
  - today's date not in tail of wiki/log.md

Audit log: ~/.claude/logs/wiki-curation-check.ndjson
"""
import json
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path


LOG_PATH = Path.home() / ".claude" / "logs" / "wiki-curation-check.ndjson"
WIKI_ROOT = Path.home() / "wiki"


def main() -> int:
    try:
        event = json.loads(sys.stdin.read())
    except Exception:
        return 0

    tool_input = event.get("tool_input") or {}
    target = tool_input.get("file_path") or tool_input.get("path") or ""
    target_norm = target.replace("\\", "/")

    if "wiki/" not in target_norm or "wiki/raw/" in target_norm:
        return 0

    findings = check(target_norm)
    if findings:
        log_entry(target_norm, findings)
        sys.stderr.write("wiki-curation-check findings:\n")
        for f in findings:
            sys.stderr.write(f"  - {f}\n")

    return 0


def check(target_norm: str) -> list[str]:
    findings: list[str] = []
    target_path = Path(target_norm)

    if not target_path.exists():
        return findings

    try:
        content = target_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    head = content[:600]
    if not head.lstrip().startswith("---"):
        findings.append("no YAML frontmatter detected")
    elif "type:" not in head:
        findings.append("frontmatter missing 'type' field")

    index_path = WIKI_ROOT / "wiki" / "index.md"
    if index_path.exists():
        index_text = index_path.read_text(encoding="utf-8", errors="replace")
        if target_path.name not in index_text:
            findings.append(f"page '{target_path.name}' not linked in wiki/index.md")

    log_path = WIKI_ROOT / "wiki" / "log.md"
    if log_path.exists():
        log_tail = log_path.read_text(encoding="utf-8", errors="replace")[-3000:]
        if date.today().isoformat() not in log_tail:
            findings.append("today's date not found in wiki/log.md tail (log_append missed?)")

    return findings


def log_entry(target: str, findings: list[str]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "target": target,
        "findings": findings,
    }
    try:
        with LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
    except Exception:
        pass


if __name__ == "__main__":
    sys.exit(main())
