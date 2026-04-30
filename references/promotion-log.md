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

## Run 2 — 2026-04-30

- Quelle: `wiki/concepts/agentic-workflow-patterns.md`
- Quellenklasse: wiki
- Laufdauer: ca. 6 Minuten
- Output verlinkt: nur in der Chat-Antwort (Inception-Test, deshalb nicht als eigenstaendige Wiki-Query gespeichert)

**Was funktionierte:**
- Quell-Variation gegen Run 1 erzwungen: TODO-Datei (Run 1) vs. Konzept-Seite (Run 2). Output-Schema hielt beiden stand.
- Manueller Naming-Collision-Check in Schritt 4 hat 4 von 6 Workflow-Kandidaten als Kollisionen erkannt (`single-loop-implementer`, `tdd`, `swarm-team-lead`, geplanter `raw-inbox-curator`). Ohne den Check waere die Empfehlung Duplikate-lastig gewesen.
- Inception-Erkennung gelang: Quelle ist selbst ein Workflow-Pattern, also ist die richtige Antwort nicht "neuen Workflow erfinden", sondern "Promotion-Checks auf vorhandene Kandidaten anwenden".
- Antwort auf eine der offenen Fragen der Quelle ("welche Workflows persistieren?") konnte konkret geliefert werden: 1 neuer Skill (`dynamic-graph-auditor`), 0 neue Hooks, 0 neue Commands.

**Was hakte:**
- Kein Standard-Archetyp aus `references/workflows.md` matchte direkt. Die Routing-Tabelle ist auf "Aufgabe trifft ein" optimiert, nicht auf "Wissensbasis mit offenen Fragen". Der Designer musste ad-hoc kombinieren (A + G), was funktionierte, aber den Schritt 2 weniger deterministisch macht.
- Inception-Bremse war manuell — der Skill-Ablauf erzwingt nicht, dass ein Designer-ueber-Designer-Lauf zu "nur Workflow, kein Skill" greift. Glueck oder Aufmerksamkeit, kein Mechanismus.
- Zwei Verdicts (`promote` fuer Multi-Agent-Codekette und Wiki-Inbox) bedeuten in Wahrheit "verweise auf bereits Existierendes" — das ist semantisch nicht `promote`, sondern eine vierte Kategorie (`already-covered` oder `link-only`). Die Verdict-Matrix kennt das nicht.

**Was fehlte:**
- Pro-Kandidat-Verdicts brauchten ein Sub-Schema, das die SKILL.md nicht vorgibt. Ich musste das Format im Lauf erfinden. Wenn Konzept-Seiten haeufiger Mehrfach-Kandidaten haben, lohnt sich ein dediziertes Sub-Schema in `references/promotion-checks.md`.
- Privacy-Klassen-Verfeinerung (Run-1-Vermutung) brauchte ich diesmal **nicht**. In beiden realen Quellen reichte "projekt". Vermutung aus Run 1 wird damit zurueckgestuft — kein V2-Vorschlag mehr.

**Anpassungs-Vorschlaege:**
- `references/workflows.md` Routing-Tabelle: 8. Eintrag "Konzept-/Wissensbasis-Seite mit offenen Promotion-Fragen" -> ad-hoc-Kombination A+G.
- `references/promotion-checks.md` Verdict-Matrix: 4. Verdict `already-covered` (oder `link-only`) ergaenzen, fuer den Fall "Kandidat existiert bereits in einem anderen Plugin/Skill, nur Backlink ziehen".
- SKILL.md Schritt 4 (Bauteil-Empfehlung): expliziten Inception-Check ergaenzen — "Beschreibt die Quelle bereits Workflow-Pattern? Dann kein neuer Skill, nur Verdicts auf vorhandene Kandidaten."
- SKILL.md Output-Schema: optionaler `## Pro-Kandidat-Verdicts`-Block fuer Quellen mit Mehrfach-Kandidaten.

## Promotion-Entscheidung

### Entscheidung — 2026-04-30

- Verdict: keep-as-pattern
- Reason: Skill funktioniert in beiden Laeufen, Output-Schema haelt zwei verschiedenen Quell-Typen stand. Aber: Run 1 und Run 2 haben jeweils Schwaechen offengelegt, die behoben werden sollten, bevor der Skill als "stable V1" gilt. Die Schwaechen sind konkret und small-scope, kein grundsaetzlicher Designfehler.
- Naechster Schritt:
  1. SKILL.md V2 mit den vier Anpassungen aus Run-1+Run-2-Logbuch (Naming-Collision-Check, Inception-Check, optionales Speicherort-Feld, optionales Pro-Kandidat-Schema).
  2. `references/workflows.md` um Routing-Eintraege fuer TODO-Dateien und Konzept-Seiten erweitern.
  3. `references/promotion-checks.md` um Verdict `already-covered` ergaenzen.
  4. Nach diesen Aenderungen Run 3 an einem dritten Quell-Typ (z. B. ein User-Inline-Text oder ein Bild) — dann Promotion-Verdict erneut pruefen.
- Aenderungen am Skill (falls keep-as-pattern): siehe oben Punkte 1-3. Sind im naechsten Pflege-Slice umsetzbar, kein Major-Refactor.

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
