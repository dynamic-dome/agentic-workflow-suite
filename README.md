# agentic-workflow-designer

Claude-Code-Skill, der unstrukturierten Input (Bilder, Notizen, Voice-Transkripte, Skizzen) in **Workflow-Blueprints** mit klaren Triggern, Schritten, Verifikation, Fehlerpfaden und einer Bauteil-Empfehlung (Skill / Command / Hook / MCP) ueberfuehrt.

## Was dieser Skill ist und nicht ist

- **Ist:** Designer. Output ist Markdown im Chat.
- **Ist nicht:** Executor. Schreibt keinen Code, keine Wiki-Seiten und keine Skills.

## Trigger

Wird ausgeloest durch Phrasen wie:

- "design a workflow"
- "turn this into a skill"
- "make a blueprint"
- "spezifiziere"
- "mach daraus ein workflow"
- "/workflow design"

Voll dokumentiert im `description`-Feld der `SKILL.md`-Frontmatter.

## Struktur

```
SKILL.md                       Entry-Point (~120 Zeilen)
references/
├── workflows.md               7 Archetypen (A-G)
├── promotion-checks.md        6 Checks fuer Skill-Promotion
├── decisions.md               D1-D4 Design-Entscheidungen
├── dco-command-spec.md        /workflow design <source> Spec
├── hooks-readonly.md          raw-write-guard, wiki-curation-check Specs
└── promotion-log.md           Logbuch fuer reale Laeufe
examples/
└── raw-image-to-workflow.md   Goldstandard-Walkthrough
```

## Installation

Lokal (nur in diesem Projekt):

```bash
ln -s "$(pwd)" ~/.claude/skills/agentic-workflow-designer
```

Global ueber das Skillschmiede-/User-Skill-Setup: siehe `~/.claude/skills/integration-guide.md`.

## Hintergrund

- Pattern-Quelle: `wiki/patterns/agentic-workflow-blueprints.md`
- TODO: `wiki/todos/2026-04-30-agentic-workflow-blueprints-umsetzen.md`
- Created: 2026-04-30

## Promotion-Status

V1 — Spec und Skill stehen, **2 reale Laeufe ausstehend** bevor Promotion-Verdict eingetragen wird. Logbuch in `references/promotion-log.md`.
