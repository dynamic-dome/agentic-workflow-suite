---
name: skill-promotion-checker
description: Use when deciding whether a recurring workflow or pattern should be codified into a real Skill, kept as a wiki pattern, or rejected. Trigger phrases - "should this become a skill", "promote this pattern", "/skill promote", "skill candidate check", "lohnt sich ein skill". Runs the 6-check promotion gate (repetition, trigger clarity, stability, context cost, testability, rollback) plus naming-collision lookup. Skip when the user has not yet run the workflow at all (premature) and skip for one-off patterns explicitly marked as such.
---

# Skill Promotion Checker

## Was dieser Skill tut

Prueft, ob ein Workflow-Pattern in einen echten Skill ueberfuehrt werden soll. Output: Verdict (`promote` / `keep-as-pattern` / `already-covered` / `reject`) mit Reason und naechstem Schritt — **keine** Skill-Erzeugung selbst.

## Wann diesen Skill nutzen

- User fragt "soll das ein Skill werden?".
- Pattern-Extractor hat einen Kandidaten gemeldet.
- Gleiche manuelle Schritte wiederholen sich seit mehreren Sessions.
- Pre-Promotion-Gate vor `skill-creator`.

**Nicht nutzen** wenn:

- Workflow ist noch nie gelaufen (Wiederholung-Check kann nicht erfuellt sein).
- Pattern ist explizit als Einmal-Aktion markiert.
- Skill ist bereits gebaut und der User will nur eine Doku-Aenderung.

## Ablauf (verbindlich)

1. **Beschreibung des Kandidaten lesen.** Trigger, Inputs, Schritte, Outputs, geschaetzte Wiederholungen.
2. **Naming-Collision-Lookup.** Vergleiche vorgeschlagenen `name` gegen `~/.claude/skills/`, gegen installierte Plugins und gegen die Archetypen aus `agentic-workflow-designer`.
3. **Die 6 Checks anwenden:**
   - Wiederholung: 3+ dokumentierte Laeufe ODER hohes Risiko.
   - Trigger-Klarheit: 3+ konkrete Trigger-Phrasen + 1 Anti-Trigger.
   - Stabilitaet: kein wesentlicher Schritt aenderte sich in den letzten 2 Laeufen.
   - Kontextkosten: SKILL.md unter ~500 Zeilen mit references/-Auslagerung moeglich.
   - Testbarkeit: mindestens 1 Beispiel-Input mit erwartetem Output.
   - Rollback: Skill schreibt nicht in irreversible Stellen ohne Bestaetigung.
4. **Anti-Pattern-Filter.** "Macht alles ein bisschen", "duplikat eines bestehenden Skills", "monatliche Pflege noetig".
5. **Quell-Klassen-Heuristik.** Wenn der Kandidat aus einer Roadmap/TODO/Konzept kommt, vergleiche mit den Tendenzen.
6. **Verdict ausgeben.**

## Output-Schema (Pflicht)

```yaml
promotion_check:
  candidate_name:
  verdict: promote | keep-as-pattern | already-covered | reject
  reason: <ein Absatz>
  checks:
    repetition: green | yellow | red
    trigger_clarity: green | yellow | red
    stability: green | yellow | red
    context_cost: green | yellow | red
    testability: green | yellow | red
    rollback: green | yellow | red
  naming_collision: <skill-name oder "keine">
  anti_patterns_hit: []
  next_step: <konkret>
```

## Verdict-Matrix

- **promote** — alle 6 Checks gruen, keine Naming-Collision, kein Anti-Pattern.
- **keep-as-pattern** — Checks 1-4 gruen, aber 5 oder 6 fehlen.
- **already-covered** — Checks waeren erfuellbar, aber bestehender Skill/Plugin deckt es ab.
- **reject** — einer der Checks 1-3 ist rot ODER Anti-Pattern getroffen.

## Akzeptanzkriterien

1. Verdict ist genau einer der vier Werte.
2. Reason hat eine konkrete Begruendung (nicht "schien gut").
3. Naming-Collision ist explizit ausgewiesen.
4. Bei `promote`: `next_step` benennt das Scaffold-Tool.
5. Bei `keep-as-pattern`: `next_step` benennt die fehlende Bedingung.
6. Bei `already-covered`: `next_step` benennt den existierenden Skill.

## Grenzen

- **Erzeugt keinen Skill.** Promotion ist Empfehlung, nicht Aktion.
- **Aktualisiert keine Plugin-Manifeste.** Das ist `skill-integrator`-Job.
- **Macht keine Tests aus.** Testbarkeits-Check ist Existenz-Frage, nicht Test-Lauf.

## Naming-Collision-Hinweis

`skill-creator` (User-Skill) macht Skill-Erstellung; dieser Skill ist das Pre-Gate davor. `plugin-optimizer` macht Multi-Skill-Optimierung; dieser Skill ist auf Einzel-Kandidaten fokussiert.
