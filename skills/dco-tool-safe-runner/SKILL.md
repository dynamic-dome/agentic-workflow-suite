---
name: dco-tool-safe-runner
description: Use when work routes through DCO (Dynamic Central Orchestrator), Telegram bot, Mini-App, or MCP tools and crosses privacy/data classification boundaries. Trigger phrases - "dco safe run", "mcp action with validation", "telegram tool gate", "/mcp safe-run", "mit tool grenzen", "privacy gate". Validates tool output before persisting to DB/wiki/answer. Skip for purely local file edits without external tools and skip when no privacy class change is involved.
---

# DCO Tool-Safe Runner

## Was dieser Skill tut

Fuehrt MCP-/Tool-/DB-/Web-Aktionen aus, die Privacy-Klassen ueberschreiten oder externe Faehigkeiten brauchen — mit Pflicht-Validierung der Tool-Ausgabe vor dem Persistieren. Output ist eine validierte Aktions-Sequenz, kein roher Tool-Output.

## Wann diesen Skill nutzen

- Aktion beruehrt MCP, externe API, DB-Schreibung oder Web/API.
- Quelle ist privat (Diary, persoenliche Notizen, Telegram-Privat).
- Aktion koennte irreversibel sein (DB-Mutation, externe Mail, Push).
- Telegram-Bot oder Mini-App-Trigger ist im Spiel.

**Nicht nutzen** wenn:

- Reine lokale Datei-Bearbeitung ohne Tool-Aufruf.
- Keine Privacy-Klassen-Ueberschreitung.
- User hat den Tool-Aufruf bereits explizit autorisiert und das Tool ist read-only.

## Ablauf (verbindlich)

1. **Intent routen.** Chat / Mini-App / Telegram / Schedule / MCP — welcher Kanal?
2. **Datenschutzklasse bestimmen.** Privat / Projekt / Oeffentlich / Operational.
3. **Toolbedarf klaeren.** Lokal / Datei / DB / MCP / Web-API.
4. **Pre-Execution-Check.**
   - Wenn private Quelle und externes Tool: STOP, expliziten Export-Befehl verlangen.
   - Wenn DB-Mutation: existiert Backup/Rollback-Pfad?
   - Wenn external API: ist die Aktion idempotent oder one-shot?
5. **Tool ausfuehren.**
6. **Tool-Output validieren.**
   - Format-Check (JSON-Struktur, erwartete Felder).
   - Plausibilitaets-Check (Werte im erwarteten Bereich).
   - Fehler-Klassifikation (transient retryable / permanent / unknown).
7. **Erst nach Validierung persistieren.** In Wiki, DB oder User-Antwort.
8. **Audit-Trail.** Eine Zeile pro Lauf in `.agent-memory/dco-actions.ndjson` mit `timestamp`, `intent`, `tool`, `privacy_class`, `verdict`. Kein Quell-Inhalt im Audit.

## Output-Schema (Pflicht)

```yaml
dco_action:
  intent: <ein Satz>
  channel: chat | mini-app | telegram | schedule | mcp
  privacy_class: privat | projekt | oeffentlich | operational
  tool_used: <name>
  pre_check:
    private_export_authorized: true | false | not-applicable
    rollback_path: <pfad oder n/a>
    idempotent: true | false
  execution:
    success: true | false
    output_validated: true | false
    error_class: transient | permanent | unknown | none
  persistence:
    written_to: <pfad oder antwort>
    audit_entry: <pfad>
```

## Pflicht-Sub-Checks

- **Privacy-Export-Gate** vor dem Tool-Aufruf — bei privaten Quellen aktivieren.
- **MCP-Output-Envelope** nach dem Tool-Aufruf — Tool-Output als untrusted markieren bis validiert.
- **Audit-Logging** auch bei Fehlschlag.

## Akzeptanzkriterien

1. Privacy-Klasse ist explizit (nicht implizit).
2. Pre-Execution-Check ist im Output sichtbar (auch bei "n/a").
3. Tool-Output ist validiert ODER der Skill stoppt mit Fehlerklasse.
4. Audit-Eintrag existiert.
5. Persistierung erfolgte erst nach Validierung, nicht parallel.

## Grenzen

- **Macht keine Code-Aenderungen.** Reine Tool-/Aktion-Ebene.
- **Erfindet keine Privacy-Klasse.** Wenn unklar, fragt der Skill nach.
- **Kein Multi-Tool-Chaining ohne expliziten Plan.** Pro Lauf ein Tool-Aufruf.

## Naming-Collision-Hinweis

`agentic-os` Plugins haben oft eigene Tool-Wrapper; dieser Skill ist die Validierungsschicht obendrauf, nicht ein Ersatz fuer die Tools selbst.
