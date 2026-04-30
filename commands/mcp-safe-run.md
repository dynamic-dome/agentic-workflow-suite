---
name: mcp-safe-run
description: Execute an MCP/external-tool action with privacy gate, output validation, and audit trail
argument-hint: <tool-name + intent>
---

# /mcp safe-run

Aktiviert den `dco-tool-safe-runner`-Skill mit dem Tool-Auftrag aus `$ARGUMENTS`.

Wenn `$ARGUMENTS` leer ist: frage nach Tool-Name und Intent.

Wenn `$ARGUMENTS` gesetzt ist:

1. Channel bestimmen (chat / mini-app / telegram / schedule / mcp).
2. Privacy-Klasse aus dem Intent ableiten.
3. Pre-Execution-Check: bei privater Quelle + externem Tool stoppen, Bestaetigung verlangen.
4. `dco-tool-safe-runner`-Skill ausfuehren.
5. Audit-Eintrag in `.agent-memory/dco-actions.ndjson`.

**Erwarteter Output:** YAML-Block mit `intent`, `tool_used`, `pre_check`, `execution`, `persistence`, `audit_entry`.
