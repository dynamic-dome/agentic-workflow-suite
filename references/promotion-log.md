# Promotion-Logbuch

Tracking der Realitaetsprobe fuer `agentic-workflow-designer`.
Ziel: nach mindestens 2 echten Laeufen die finale Promotion-Entscheidung dokumentieren — laut TODO `wiki/wiki/todos/2026-04-30-agentic-workflow-blueprints-umsetzen.md` Akzeptanz-Kriterium.

## Run-Schema

Pro Lauf eine Sektion mit folgendem Schema:

```markdown
### Run N — YYYY-MM-DD

- Quelle: <pfad oder beschreibung>
- Quellenklasse: raw | wiki | repo | chat | external
- Laufdauer: ca. X Minuten
- Output verlinkt: <pfad zum gespeicherten blueprint, falls vorhanden>

**Was funktionierte:**
- ...

**Was hakte:**
- ...

**Was fehlte:**
- ...

**Anpassungs-Vorschlaege:**
- konkret an SKILL.md / references/...
```

## Run 1 — _offen_

Wird beim ersten echten Lauf des Designers ausgefuellt.

## Run 2 — _offen_

Wird beim zweiten echten Lauf des Designers ausgefuellt.

## Promotion-Entscheidung

Wird nach mindestens 2 Runs eingetragen. Schema:

```markdown
### Entscheidung — YYYY-MM-DD

- Verdict: promote | keep-as-pattern | reject | needs-more-data
- Reason: <warum>
- Naechster Schritt: <konkret>
- Aenderungen am Skill (falls keep-as-pattern): <was muss noch ueberarbeitet werden>
```

## Was diesen Skill **nicht** weiter promoted

Promotion stoppen, wenn auch nur einer dieser Punkte zutrifft (siehe `references/promotion-checks.md`):

- Trigger ist nach 2 Laeufen immer noch ueberlappend mit anderen Skills.
- Output ist in 50%+ der Laeufe unvollstaendig (Pflicht-Block leer).
- User musste den Skill in beiden Laeufen substantiell korrigieren, bevor das Ergebnis brauchbar war.
- Designer empfiehlt in fast jedem Lauf "promote" — das deutet auf zu lockere Checks hin, nicht auf einen tollen Skill.

## Wer fuehrt das Logbuch?

- Der User, am Ende eines Laufs, mit den 4 Bullet-Listen.
- Optional: Claude bietet am Ende eines Designer-Laufs an, den Logeintrag fuer den User vorzubereiten.

## Wo liegen die Outputs der Laeufe?

- Vorschlag: `wiki/queries/YYYY-MM-DD-workflow-design-<slug>.md` mit Frontmatter `type: query`, `tags: [workflow-design, designer-run]`.
- Im Logbuch hier: nur Pfad-Verweis, nicht den ganzen Output duplizieren.
