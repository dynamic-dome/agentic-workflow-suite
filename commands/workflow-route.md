---
name: workflow-route
description: Decide which working mode (A-G) fits a given request before doing any work
argument-hint: <request — was soll passieren>
---

# /workflow route

Aktiviert den `workflow-router`-Skill mit der Anfrage aus `$ARGUMENTS`.

Wenn `$ARGUMENTS` leer ist: frage den User, was er erreichen will.

Wenn `$ARGUMENTS` gesetzt ist:

1. Eingabe an `workflow-router` weitergeben.
2. Output ist eine Routing-Entscheidung mit Archetyp, Risiko, Artefakten und `next_skill`.
3. Den `next_skill` **nicht automatisch ausfuehren** — Empfehlung an den User.

**Erwarteter Output:** YAML-Block mit `archetype`, `risk`, `next_skill`, `stop_criteria`.
