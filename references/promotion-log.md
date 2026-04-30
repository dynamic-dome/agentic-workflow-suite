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

## Run 3 — 2026-04-30

- Quelle: `Desktop/Claude-Plugins-Skills/PLUGIN-SKILL-IMPROVEMENT-ROADMAP-2026-04-30.md`
- Quellenklasse: repo (445 Zeilen Markdown ohne Frontmatter, Roadmap mit Phasen 0-5 + Work-Packages)
- Laufdauer: ca. 8 Minuten
- Output verlinkt: nur in der Chat-Antwort (nicht als Wiki-Query gespeichert; Quelle ist Repo, nicht Wiki — Speicherort-Block wuerde hier auf `wiki/queries/` zeigen, aber User entscheidet)

**Was funktionierte:**
- Erster Lauf nach V2. **Naming-Collision-Check griff automatisch** (Schritt 4 zwingt es) und fand 4+ Kollisionen in den Phasen 1, 2, 5 und WP3. Ohne V2 waere der Designer blind durchgelaufen.
- **Inception-Check griff automatisch** und verhinderte eine Selbst-Empfehlung (`agentic-workflow-designer` ist Teil des in der Roadmap beschriebenen Oekosystems).
- **Optionaler `Pro-Kandidat-Verdicts`-Block** war hier genau richtig: 9 Kandidaten (6 Phasen + 3 Work-Packages), pro Kandidat ein Mini-Verdict. Die V2-Schema-Erweiterung hat sich an einem realen Fall bewiesen.
- **Verdict-Werte sind ausgewogen:** 4x already-covered, 2x keep-as-pattern, 2x reject, 1x promote-als-Script, 1x reject fuer den Top-Level-Skill selbst. Das ist gesunde Empirie ueber das Oekosystem, kein "alles ist toll"-Bias.
- **Routing-Tabelle** lieferte sauber Workflow C (Dynamic-Graph-Audit) als Primaer, mit B-Anteilen pro Work-Package.

**Was hakte:**
- **Bauteil-Ebene `Script` fehlt.** Phase 4 verlangt nach `scripts/plugin_ecosystem_smoke.ps1` — das ist ein Promotion-Kandidat, aber kein Skill, kein Command, kein Hook und kein MCP. Im Lauf habe ich es manuell als "kein Skill, sondern Script" markiert. SKILL.md kennt nur 5 Ebenen (`Skill | Command | Hook | MCP-Contract | nur Workflow`). V3-Vorschlag.
- **Phasen ohne Frontmatter:** die Quelle hat keine maschinenlesbaren Tags, also musste die Phasen-Aufzaehlung manuell aus dem Markdown extrahiert werden. Bei sehr grossen Quellen (>1000 Zeilen) koennte das zur Schwachstelle werden. Heute irrelevant.

**Was fehlte:**
- Kein Mechanismus, um zu erkennen, dass die Roadmap **selbst ein Audit-Ergebnis** ist (Workflow C wurde bereits gelaufen). Der Designer kann zwar die Quelle als "Audit-Ergebnis" lesen, hat aber keinen expliziten Schritt dafuer. Bei wiederholten Roadmap-Inputs koennte das verwirren — aber der Inception-Check bremst es bereits indirekt.

**Anpassungs-Vorschlaege (V3):**
- SKILL.md Bauteil-Ebenen erweitern: 5. Wert `Script` hinzufuegen, fuer Skript-Kandidaten die kein Skill rechtfertigen.
- `references/workflows.md` Routing-Tabelle: 10. Eintrag "Roadmap-/Phasenplan-Datei (Markdown ohne Frontmatter, mehrphasig, Deliverables pro Phase)" -> C+B ad-hoc.
- Optional: `references/promotion-checks.md` koennte einen expliziten "Quell-Klasse"-Filter bekommen (Roadmap-Quellen sind per se selten promote-Kandidaten; Trigger-Klarheit ist bei Single-Use-Roadmaps niedrig).

## Promotion-Entscheidung — Final

### Entscheidung — 2026-04-30 (nach Run 3)

- Verdict: **promote**
- Reason: Drei Laeufe an drei kategorisch unterschiedlichen Quell-Typen (TODO-Datei, Konzept-Seite, Roadmap-Markdown). Alle 3 produzierten vollstaendige Outputs nach Pflicht-Schema. V2-Sub-Checks (Inception, Naming-Collision) griffen in Run 3 automatisch und ersetzten die manuelle Arbeit aus Run 1+2. Verdict-Verteilung ueber Run 3 (4x already-covered, 2x keep-as-pattern, 2x reject, 1x promote) ist ausgewogen und zeigt nicht das "Designer empfiehlt immer promote"-Anti-Pattern. Promotion-Checks-Liste ist erfuellt:
  - Wiederholung: 3 Laeufe ✅
  - Trigger-Klarheit: 7+ Trigger-Phrasen + Anti-Trigger ✅
  - Stabilitaet: Output-Schema unveraendert seit V1, V2 nur erweitert ✅
  - Kontextkosten: SKILL.md 141 Zeilen ✅
  - Testbarkeit: 3 reale Beispiele + 1 Goldstandard-Walkthrough ✅
  - Rollback: read-only auf Quellen, schreibt nichts ✅
- Naechster Schritt:
  1. **V3 separat** (kein Blocker fuer Promotion): `Script` als 5. Bauteil-Ebene in SKILL.md, Roadmap-Eintrag in der Routing-Tabelle. Klein, in einem Slice umsetzbar.
  2. **Plugin-/Marketplace-Frage** wieder anpacken — das Repo ist jetzt promote-reif, also eigenstaendige `plugin.json` + Marketplace-Eintrag wird sinnvoll.
  3. **Run 4+** spontan, wenn ein neuer Quell-Typ vorbeikommt (z. B. Bild, Voice-Transkript, externe URL). Kein zwingender naechster Schritt; der Skill ist im Wildbetrieb-Modus.

**Promotion-Status des Skills:** stabil V2, promote-reif, keine offenen Designfehler. V3-Punkte sind Pflege, keine Notwendigkeit.

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
