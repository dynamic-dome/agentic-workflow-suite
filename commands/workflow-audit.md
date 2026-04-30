---
name: workflow-audit
description: Run a dynamic-graph audit on a broad scope (plugin ecosystem, wiki cluster, repo monorepo)
argument-hint: <scope — pfad oder cluster-name>
---

# /workflow audit

Aktiviert den `dynamic-graph-auditor`-Skill mit dem Scope aus `$ARGUMENTS`.

Wenn `$ARGUMENTS` leer ist: frage den User nach dem Scope (Pfad-Glob oder explizite Verzeichnis-Liste).

Wenn `$ARGUMENTS` gesetzt ist:

1. Scope validieren (existiert der Pfad? wie viele Files?).
2. Bei mehr als 500 Files: Sampling vorschlagen, sonst direkt durchlaufen.
3. `dynamic-graph-auditor`-Skill aufrufen.
4. Output ist ein Audit-Report mit Inventar, Clustern, Redundanzen und priorisierten TODOs.

**Erwarteter Output:** YAML-Block + optional Mermaid-Cluster-Graph.
