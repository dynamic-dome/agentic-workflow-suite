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

## Run 1 — 2026-04-30

- Quelle: `wiki/wiki/todos/2026-04-30-agentic-workflow-blueprints-umsetzen.md`
- Quellenklasse: wiki
- Laufdauer: ca. 4 Minuten (synchron mit Skill-Bauarbeit)
- Output verlinkt: nur in der Chat-Antwort dokumentiert (noch nicht als Wiki-Query gespeichert)

**Was funktionierte:**
- 6-Schritt-Ablauf in der SKILL.md liess sich linear abarbeiten, ohne Spruenge.
- Output-Schema ist vollstaendig nutzbar — alle Pflicht-Bloecke wurden ohne Leerlauf gefuellt.
- Routing-Tabelle in `references/workflows.md` half, schnell auf Workflow B (Single-Loop) zu kommen.
- Selbstpruefung gegen Akzeptanzkriterien am Ende ist ein guter Anker.

**Was hakte:**
- Der vorgeschlagene Skill-Name (`pattern-todo-implementer`) ueberlappt semantisch mit `single-loop-implementer` aus den Archetypen. Der Designer hat das nicht selbst erkannt; ich habe es manuell in der Selbstpruefung notiert. Hinweis: Schritt 4 des Ablaufs ("Bauteil-Empfehlung") sollte einen expliziten Sub-Check haben "Ueberlappt der vorgeschlagene Name mit existierenden Skill-Kandidaten in workflows.md?".
- Privacy-Klasse "projekt" war hier richtig, aber das Schema unterscheidet nicht zwischen "wiki public" und "wiki nur lokal" — koennte in Run 2 wichtig werden, wenn jemand eine Raw-Inbox-Datei hineinwirft.

**Was fehlte:**
- Es gibt keinen vorgesehenen Speicherort fuer den Designer-Output. `examples/raw-image-to-workflow.md` zeigt ihn als Markdown-Block, aber ein realer Lauf produziert keine Datei. Vorschlag fuer Run 2: Designer empfiehlt am Ende einen Pfad (z. B. `wiki/queries/YYYY-MM-DD-workflow-design-<slug>.md`) und der User entscheidet, ob er den Output dort ablegt.

**Anpassungs-Vorschlaege:**
- SKILL.md Ablauf-Schritt 4: ergaenzen um Naming-Collision-Check gegen `references/workflows.md`.
- references/workflows.md Routing-Tabelle: einen achten Eintrag "TODO-Datei mit applies_to:" hinzufuegen, der zu Workflow B routet.
- SKILL.md Output-Schema: optionalen `## Speicherort`-Block hinzufuegen (Vorschlag wo der Output abgelegt werden koennte).

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
