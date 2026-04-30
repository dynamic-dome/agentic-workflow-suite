---
name: workflow-router
description: Use when the user has an unclear request and you need to decide which working mode applies before doing anything else. Trigger phrases - "which workflow fits", "how should I approach this", "route this", "wie angehen", "welcher workflow", "mach plan". Returns one of seven archetypes plus risk class, expected artifacts, verification plan, and stop criteria. Skip when the user has already named a clear task and the route is obvious.
---

# Workflow Router

## Was dieser Skill tut

Routet eine Anfrage in einen der 7 Workflow-Archetypen aus dem `agentic-workflow-designer`-Pattern (A-G). Output ist eine Routing-Entscheidung mit Risiko-Klasse, erwarteten Artefakten und Stop-Kriterien — **keine Ausfuehrung**, nur Routing.

## Wann diesen Skill nutzen

- User-Anfrage ist mehrdeutig: "mach was draus", "schau mal", "kannst du helfen mit X".
- DCO/Mini-App/Telegram/Hook gibt einen Raw-Input weiter und du sollst entscheiden, was damit passiert.
- Du selbst bist unsicher, ob das ein Audit, ein Patch, eine Wiki-Kuratierung oder ein Skill-Promotion-Check werden soll.

**Nicht nutzen** wenn:

- Aufgabe ist offensichtlich (z. B. "fix typo in README" -> Workflow B direkt).
- Es geht nicht um Routing, sondern um eine konkrete Antwort auf eine Wissensfrage.

## Ablauf (verbindlich)

1. **Input-Typ bestimmen.** Code, Wiki, Raw-Inbox, Bild, Plan, Security, DCO/MCP, Konzept, Roadmap, TODO, andere.
2. **Ziel bestimmen.** Antwort, Datei, Wiki-Seite, Code-Patch, Skill-Blueprint, echter Skill, Audit-Report.
3. **Risiko bestimmen.** read-only / write / privacy / security / external-tool / irreversible.
4. **Archetyp waehlen.** Genau einer aus A-G (siehe Output-Schema). Wenn keiner passt, ad-hoc kombinieren und begruenden.
5. **Stop-Kriterien notieren.** Ab wann ist die Aufgabe erledigt oder muss eskalieren.
6. **An naechsten Workflow uebergeben.** Nicht selbst ausfuehren — nur Empfehlung.

## Output-Schema (Pflicht)

```yaml
workflow_route:
  input_type: code | wiki | raw-inbox | bild | plan | security | dco-mcp | konzept | roadmap | todo | inline
  goal: <ein Satz>
  risk: low | medium | high
  archetype: A-Intake-Router | B-Single-Loop | C-Dynamic-Graph-Audit | D-Review-Fix-Verify | E-Raw-to-Wiki | F-DCO-Tool-Safe | G-Skill-Promotion | ad-hoc
  reason: <ein Satz, warum dieser Archetyp>
  artifacts:
    - <pfad oder beschreibung>
  verification:
    - <konkrete Checks>
  stop_criteria:
    - <wann ist Schluss>
  next_skill: <Skill-Name aus dem Plugin oder "manual">
```

## Beispiele

**Eingabe:** "Hier ist eine TODO-Datei aus dem Wiki, mach was draus."
**Routing:** input_type=todo, archetype=B-Single-Loop, next_skill=agentic-workflow-designer.

**Eingabe:** "Schau dir das ganze Plugin-Oekosystem an."
**Routing:** input_type=plan, archetype=C-Dynamic-Graph-Audit, next_skill=dynamic-graph-auditor.

**Eingabe:** "Ich hab grad einen Patch geschrieben, kannst du draufschauen?"
**Routing:** input_type=code, archetype=D-Review-Fix-Verify, next_skill=review-fix-verify-loop.

## Grenzen

- **Macht keine Inhaltsentscheidungen.** Das ist Job des nachgeschalteten Skills.
- **Wenn der Input bereits eindeutig geroutet ist:** Skill empfiehlt das Skip — keine Pseudo-Routing-Begruendung.
- **Mehrdeutige Inputs werden als ad-hoc markiert**, nicht erzwungen-zugeordnet.

## Akzeptanzkriterien

1. Genau ein Archetyp ist ausgewaehlt (oder `ad-hoc` mit Begruendung).
2. Risiko-Klasse ist explizit.
3. `next_skill` ist konkret benannt (oder `manual`, wenn kein Skill passt).
4. Stop-Kriterien sind nicht-leer.
