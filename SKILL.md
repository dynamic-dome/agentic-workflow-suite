---
name: agentic-workflow-designer
description: Use when the user wants to turn a rough idea, screenshot, diagram, voice note, raw inbox file, or hand-drawn sketch into a concrete agentic workflow with triggers, inputs, steps, verification, error paths, and a Skill/Command/Hook/MCP recommendation. Trigger phrases - "design a workflow", "turn this into a skill", "make a blueprint", "spezifiziere", "mach daraus ein workflow", "skill blueprint", "/workflow design". Do NOT use this skill to execute workflows or write production code; the output is a blueprint, not an implementation. Also skip when the user only wants a diagram and is not asking for a runnable agentic process.
---

# Agentic Workflow Designer

## Was dieser Skill tut

Aus unstrukturiertem Input (Bild, Notiz, Voice-Transkript, Wiki-Seite, vager Idee) entsteht ein **Workflow-Blueprint** mit:

- explizitem Trigger
- Inputs und erwarteten Outputs
- Schritten in einer eindeutigen Reihenfolge
- Verifikationspunkten
- Fehlerpfaden
- Empfehlung: Skill, Command, Hook oder MCP-Contract
- Promotion-Verdict (`promote` / `keep-as-pattern` / `reject`)

Der Skill **erzeugt keine echten Skill-Dateien**. Er erzeugt einen Bauplan, den der User danach explizit in eine Runtime promoten kann (z. B. via `skill-creator` oder Plugin-Workflow).

## Wann diesen Skill nutzen

- User zeigt ein Bild, Diagramm oder Screenshot und sagt "mach daraus etwas".
- User hat eine Raw-Notiz aus der Obsidian-Inbox und will sie in einen wiederholbaren Prozess verwandeln.
- User beschreibt einen halb-stabilen Ablauf, den er schon mehrmals haendisch gemacht hat.
- User fragt "soll das ein Skill werden?" oder "welcher Workflow passt hier?".

**Nicht nutzen** wenn:

- User will direkt Code schreiben oder einen bestehenden Skill ausfuehren.
- Es gibt bereits einen gepflegten Workflow-Plan und nur die Implementierung fehlt.
- User will nur ein Diagramm oder eine Visualisierung, keinen Ablauf.

## Ablauf (verbindlich)

Folge diesen 6 Schritten in dieser Reihenfolge. Spring nicht vor.

1. **Quelle lesen.** Bild beschreiben, Datei zitieren, Wiki-Seite holen, Notiz uebernehmen. **Beobachtung und Interpretation getrennt halten** — erst was steht da, dann was bedeutet das.
2. **Workflow-Typ routen.** Lies `references/workflows.md` und waehle einen der 7 Archetypen (A-G). Wenn nichts passt, baue einen neuen Workflow ad hoc, aber begruende warum keiner der 7 ausreicht.
3. **Blueprint schreiben.** Folge dem Output-Schema unten. Jeder Pflicht-Block ist nicht-leer. Mermaid ist optional, kein Ersatz fuer Text.
4. **Bauteil-Empfehlung.** Eines aus `Skill | Command | Hook | MCP-Contract | nur Workflow`. Begruendung in einem Satz: warum diese Ebene, nicht eine andere.
5. **Promotion-Check.** Lies `references/promotion-checks.md` und gib ein Verdict aus.
6. **Grenzen markieren.** Wenn die Quelle privat oder Raw-Inbox ist: Privacy-Hinweis ergaenzen, Raw-Pfad nicht mutieren.

## Output-Schema (Pflicht)

Jeder Lauf produziert genau diese Struktur als Markdown-Antwort:

```markdown
# Workflow-Blueprint: <Name>

## Quelle
- Pfad oder Beschreibung
- Quellenklasse: raw | wiki | repo | chat | external
- Privacy: privat | projekt | oeffentlich

## Beobachtung
<Was ist im Input zu sehen — ohne Interpretation>

## Ableitung
<Was bedeutet das — getrennt von Beobachtung>

## Workflow
- Trigger:
- Inputs:
- Rollen:
- Ablauf:
  1. ...
- Entscheidungspunkte:
- Verifikation:
- Fehlerpfade:

## Bauteil-Empfehlung
- Ebene: Skill | Command | Hook | MCP-Contract | nur Workflow
- Begruendung (1 Satz):
- Wenn Skill: vorgeschlagener `name` und `description`-Trigger.

## Promotion
- Verdict: promote | keep-as-pattern | reject
- Reason:
- Naechster Schritt:

## Grenzen
- Was dieser Workflow NICHT macht.
- Welche Risiken offen bleiben.
```

## Referenzen

Tiefe ist ausgelagert, damit dieser SKILL.md schlank bleibt:

- `references/workflows.md` — die 7 Archetypen (Intake-Router, Single-Loop, Dynamic-Graph-Audit, Review-Fix-Verify, Raw-to-Wiki, DCO-Tool-Safe, Skill-Promotion).
- `references/promotion-checks.md` — Kriterien fuer das Promotion-Verdict.
- `references/decisions.md` — getroffene Design-Entscheidungen (z. B. raw-inbox-curator-Frage).
- `references/dco-command-spec.md` — wie `/workflow design <source>` als Command aufgesetzt werden soll.
- `references/hooks-readonly.md` — read-only Checker-Hooks fuer raw-write-guard und wiki-curation-check.
- `references/promotion-log.md` — Logbuch fuer reale Laeufe und finale Promotion-Entscheidung.
- `examples/raw-image-to-workflow.md` — Walkthrough an einem echten Beispiel.

## Grenzen dieses Skills

- **Schreibt keine Wiki-Seiten und keinen Code.** Output ist Markdown im Chat.
- **Mutiert keine Raw-Inbox-Dateien.** Wenn Input eine Raw-Datei ist, wird sie nur gelesen und zitiert.
- **Macht keine Multi-Agent-Orchestrierung.** Wenn ein Workflow nach Multi-Agent verlangt, wird das im Blueprint markiert, aber der Skill bleibt single-agent.
- **Ist kein Promotion-Executor.** Das Verdict `promote` ist eine Empfehlung; der User entscheidet und startet die Promotion separat.

## Akzeptanzkriterien

Ein Lauf gilt als erfolgreich, wenn:

1. Beobachtung und Ableitung sind klar getrennt.
2. Alle Pflicht-Bloecke des Output-Schemas sind nicht-leer.
3. Die Bauteil-Empfehlung hat eine Begruendung.
4. Das Promotion-Verdict hat einen Reason.
5. Privacy-Klasse ist explizit, nicht implizit.

Wenn auch nur einer dieser Punkte fehlt, ist der Output unvollstaendig — Skill nochmal laufen lassen oder Luecke nachreichen.
