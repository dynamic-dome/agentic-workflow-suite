# agentic-workflow-suite

A Claude Code plugin that turns rough ideas, raw inbox material, and ad-hoc workflows into a coherent operating system for agentic work — with **7 skills**, **7 slash commands**, and **5 read-only checker hooks**.

Built from `wiki/patterns/agentic-workflow-blueprints.md`. Tested through 3 real designer runs (TODO file, concept page, multi-phase roadmap) before being expanded into a full plugin.

## Was die Suite tut

| Layer | Bausteine |
|---|---|
| **Skills** (7) | `agentic-workflow-designer`, `workflow-router`, `raw-inbox-curator`, `dynamic-graph-auditor`, `review-fix-verify-loop`, `dco-tool-safe-runner`, `skill-promotion-checker` |
| **Slash Commands** (7) | `/workflow design`, `/workflow route`, `/workflow audit`, `/wiki curate`, `/review-loop`, `/skill promote`, `/mcp safe-run` |
| **Hooks** (5, read-only) | `raw-write-guard`, `wiki-curation-check`, `mcp-output-envelope`, `private-export-gate`, `workflow-wrap-up` |

## Wann dieses Plugin nutzen

- Du hast eine grobe Idee, einen Screenshot, eine Voice-Notiz oder eine Pattern-Seite und willst daraus einen wiederholbaren Workflow.
- Du arbeitest an einem grossen Repo-/Plugin-/Wiki-Oekosystem und brauchst Audits, Review-Loops und Privacy-Gates.
- Du willst Raw-Inbox-Material kontrolliert ins Wiki ueberfuehren.
- Du willst Promotion-Entscheidungen ("soll das ein Skill werden?") nach harten Checks treffen, nicht nach Bauchgefuehl.

## Skill-Uebersicht

| Skill | Zweck | Output |
|---|---|---|
| `agentic-workflow-designer` | Quelle -> Workflow-Blueprint mit Bauteil-Empfehlung | Markdown-Block mit Schema |
| `workflow-router` | Anfrage -> Archetyp-Routing (A-G) | YAML mit `archetype`, `risk`, `next_skill` |
| `raw-inbox-curator` | Raw-Datei -> kuratierte Wiki-Seite | Neue Wiki-Seite + Index/Log-Updates |
| `dynamic-graph-auditor` | Scope -> Inventar + Cluster + Redundanzen + TODOs | YAML-Audit-Report + optionaler Mermaid |
| `review-fix-verify-loop` | Patch -> Findings -> Fixes -> Verifikation | YAML mit getrennten Phasen |
| `dco-tool-safe-runner` | MCP-/Tool-Aktion mit Privacy-Gate + Validierung | YAML mit Audit-Trail |
| `skill-promotion-checker` | Pattern -> Promotion-Verdict (4 Werte) | YAML mit `verdict`, 6 Checks, Naming-Collision |

## Hook-Modi (V2 read-only Checker)

Alle Hooks **warnen, blocken nicht**. Sie schreiben Audit-Logs unter `~/.claude/logs/<hook-name>.ndjson`. Promotion-Pfad zu echten Block-Hooks erst nach 10+ false-positive-freien Laeufen — siehe `skills/agentic-workflow-designer/references/hooks-readonly.md`.

| Hook | Event | Was er prueft |
|---|---|---|
| `raw-write-guard` | PreToolUse (Write/Edit/...) | Ziel ist nicht in `wiki/raw/` |
| `wiki-curation-check` | PostToolUse (Wiki-Write) | Frontmatter, Index-Link, Log-Eintrag |
| `mcp-output-envelope` | PostToolUse (mcp__*) | MCP-Output als untrusted markieren |
| `private-export-gate` | PreToolUse (Export-Tools) | Privacy-Klasse der Quelle |
| `workflow-wrap-up` | Stop | Reminder fuer Wrap-up |

## Installation

### Variante A — als Plugin via Marketplace

```bash
claude plugin marketplace add willneverusegit/agentic-workflow-suite
claude plugin install agentic-workflow-suite
```

### Variante B — lokal als Plugin-Repo

```bash
# In einem beliebigen Projekt-Root:
git clone https://github.com/willneverusegit/agentic-workflow-suite.git
# Plugin von einem lokalen Pfad referenzieren:
claude plugin install agentic-workflow-suite --from ./agentic-workflow-suite
```

### Variante C — einzelner Skill via Symlink

```bash
ln -s "$(pwd)/skills/agentic-workflow-designer" ~/.claude/skills/agentic-workflow-designer
```

## Hooks aktivieren

Hooks sind **opt-in**. Konfiguration in `hooks/hooks.json` einsehen, dann gewuenschte Eintraege in deine `~/.claude/settings.json` (oder Projekt-`.claude/settings.json`) uebernehmen — nicht alle muessen aktiviert sein.

## Verzeichnisstruktur

```
.claude-plugin/
└── plugin.json                         Plugin-Manifest
skills/
├── agentic-workflow-designer/          Hauptdesigner mit references/ + examples/
├── workflow-router/
├── raw-inbox-curator/
├── dynamic-graph-auditor/
├── review-fix-verify-loop/
├── dco-tool-safe-runner/
└── skill-promotion-checker/
commands/
├── workflow-design.md                  /workflow design <source>
├── workflow-route.md                   /workflow route <request>
├── workflow-audit.md                   /workflow audit <scope>
├── wiki-curate.md                      /wiki curate <raw-pfad>
├── review-loop.md                      /review-loop <scope>
├── skill-promote.md                    /skill promote <pattern>
└── mcp-safe-run.md                     /mcp safe-run <tool+intent>
hooks/
├── hooks.json                          Settings-Snippet
├── raw-write-guard.py
├── wiki-curation-check.py
├── mcp-output-envelope.py
├── private-export-gate.py
└── workflow-wrap-up.py
```

## Empirie hinter dem Plugin

Der Hauptdesigner durchlief vor dem Plugin-Bundle drei dokumentierte Realitaetslaufe:

| Run | Quelle | Verdict | Erkenntnis |
|---|---|---|---|
| 1 | TODO-Datei | keep-as-pattern | Naming-Collision-Check fehlte |
| 2 | Konzept-Seite | keep-as-pattern | Inception-Check fehlte |
| 3 | Plugin-Roadmap | promote | V2-Sub-Checks griffen automatisch, Bauteil-Ebene `Script` ergaenzt |

Vollstaendiges Logbuch: [`skills/agentic-workflow-designer/references/promotion-log.md`](skills/agentic-workflow-designer/references/promotion-log.md)

## Hintergrund und Quellen

- Pattern-Seite: `wiki/patterns/agentic-workflow-blueprints.md`
- Zugrundeliegendes Konzept: `wiki/concepts/agentic-workflow-patterns.md`
- TODO-Origin: `wiki/todos/2026-04-30-agentic-workflow-blueprints-umsetzen.md`
- Created: 2026-04-30
- Version: `1.0.0`

## Lizenz

MIT.
