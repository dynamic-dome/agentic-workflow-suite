# Hook-Design: Read-only Checker

**Status:** Spezifikation. Implementierung erst nach 2-3 echten Designer-Laeufen, wenn Telemetrie zeigt, **was** ueberhaupt warnungswuerdig ist.

**Modus:** Beide Hooks **warnen nur**, blocken nichts. Begruendung in `references/decisions.md` D2.

## Hook 1 — `raw-write-guard`

**Event:** `PreToolUse` mit `tool ∈ {Write, Edit, NotebookEdit, mcp__wiki__wiki_write, mcp__wiki__wiki_append_section}`.

**Zweck:** Warnen, wenn ein Schreibversuch auf einen Pfad in `wiki/raw/` zielt.

**Pseudo-Logik:**

```python
def raw_write_guard(event):
    target = event.tool_input.get("file_path") or event.tool_input.get("path")
    if not target:
        return ALLOW

    if "wiki/raw/" in target.replace("\\", "/"):
        return WARN(
            f"Schreibversuch auf Raw-Inbox: {target}. "
            f"Raw-Dateien werden nur gelesen, nicht mutiert. "
            f"Wenn das Absicht ist, bestaetige im Chat."
        )

    return ALLOW
```

**Output:** Eine Warning-Zeile in den Chat **vor** der Tool-Ausfuehrung. Tool laeuft trotzdem durch (Read-Only-Checker, kein Block).

**Audit:**

- Eintrag in `~/.claude/logs/raw-write-guard.ndjson` mit `timestamp`, `target`, `tool`, `decision`.
- Nach 10 Eintraegen: schauen, ob die Warnung jemals false-positive war. Wenn nein: in V2 zu `BLOCK` upgraden.

**Was der Hook NICHT tut:**

- Nicht die Datei lesen oder pruefen.
- Nicht raten, ob die Aenderung "okay" ist.
- Nicht den Workflow durcheinander bringen — Warning ist informativ.

## Hook 2 — `wiki-curation-check`

**Event:** `PostToolUse` mit `tool ∈ {mcp__wiki__wiki_write, mcp__wiki__wiki_append_section}`.

**Zweck:** Nach jedem Wiki-Schreibvorgang pruefen, ob die Hygiene stimmt — Frontmatter da, Index aktualisiert, Log eingetragen, Raw-Quelle referenziert (falls aus Raw-Inbox).

**Pseudo-Logik:**

```python
def wiki_curation_check(event):
    target = event.tool_input.get("path", "")
    if not target.startswith("wiki/") or "raw/" in target:
        return ALLOW  # nur kuratierte Wiki-Seiten pruefen

    findings = []

    content = read_file(target)
    if not content.startswith("---"):
        findings.append("Kein YAML-Frontmatter erkannt.")

    if "type:" not in content[:500]:
        findings.append("Frontmatter ohne 'type'-Feld.")

    index = read_file("wiki/index.md")
    target_basename = path_basename(target)
    if target_basename not in index:
        findings.append(f"Seite nicht in wiki/index.md verlinkt.")

    log = read_file("wiki/log.md")
    today = today_iso()
    if today not in log[-2000:]:
        findings.append("Heutiges Datum nicht im wiki/log.md gefunden — ggf. log_append vergessen.")

    if findings:
        return WARN("Wiki-Curation-Check Findings:\n- " + "\n- ".join(findings))

    return ALLOW
```

**Output:** Liste der Findings als Chat-Warnung. Schreibvorgang ist bereits durchgelaufen, der Hook signalisiert "schau nochmal drauf".

**Audit:**

- Eintrag in `~/.claude/logs/wiki-curation-check.ndjson` mit `timestamp`, `target`, `findings`.
- Trend ueber 20 Laeufe: welche Findings tauchen oft auf? Daraus folgt, welche Hilfsfunktionen (`log_append`, `wiki_append_section`) staerker beworben werden sollten.

**Was der Hook NICHT tut:**

- Nicht den Index oder das Log selbst aktualisieren — das ist der Job des Schreibers.
- Nicht den Inhalt bewerten (Qualitaet, Sprachstil, Cluster-Zuordnung).
- Nicht Frontmatter-Werte validieren (kein Schema-Check), nur Vorhandensein.

## Konfiguration

In `.claude/settings.json` zu ergaenzen, wenn die Hooks live gehen:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|NotebookEdit|mcp__wiki__wiki_write|mcp__wiki__wiki_append_section",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/scripts/raw-write-guard.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "mcp__wiki__wiki_write|mcp__wiki__wiki_append_section",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/scripts/wiki-curation-check.py"
          }
        ]
      }
    ]
  }
}
```

## Promotion-Pfad

| Stufe | Verhalten | Trigger zum Aufstieg |
|---|---|---|
| V1 (jetzt) | Spec only, kein Code | `agentic-workflow-designer` lief 2-3 mal real |
| V2 | Read-only Checker, warn-only | Designer hat Konzept bewiesen, Wiki-Schreibungen passieren regelmaessig |
| V3 | `raw-write-guard` blockt; `wiki-curation-check` bleibt warn | 10+ Hook-Laeufe ohne false-positive |
| V4 | Beide blocken, mit explizitem Override-Flag | Hooks haben sich in V3 als zuverlaessig erwiesen |

**Aufstieg jeweils nur mit Telemetrie-Beleg, nicht aus Bauchgefuehl.**

## Was diese Spec NICHT abdeckt

- `mcp-output-envelope` und `private-export-gate` aus dem Pattern-Dokument — separates Hook-Slice, weil sie MCP-tief greifen und V1-Designer noch nichts mit MCP macht.
- `workflow-wrap-up` Hook — gehoert zum DCO-Wrap-up-System, nicht zum Designer-Skill.
- Settings-Merge-Strategie wenn der User schon eigene Hooks hat — siehe `update-config` Skill.
