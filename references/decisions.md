# Design-Entscheidungen

## D1 — `raw-inbox-curator` als eigener Skill, nicht als Modus

**Datum:** 2026-04-30
**Frage:** Soll `raw-inbox-curator` ein eigener Skill werden oder ein Referenzmodus innerhalb des `agentic-workflow-designer`?

**Entscheidung:** Eigener Skill, separat zu bauen — aber **nicht in dieser TODO-Iteration**.

**Begruendung:**

| Kriterium | Wuerde `agentic-workflow-designer` das gut tun? | Wuerde ein eigener `raw-inbox-curator` das besser tun? |
|---|---|---|
| Output-Typ | Designer produziert **Markdown im Chat**. | Curator produziert **echte Wiki-Files** auf der Platte. |
| Risiko | Read-only auf Raw-Quelle. | Schreibt nach `wiki/`, beruehrt `index.md` und `log.md`. |
| Trigger | "design a workflow", "blueprint". | "ins wiki schreiben", "kurate die raw-datei". |
| Wiederholungswert | Hoch — ein Skill fuer alle Workflow-Quellen. | Hoch — ein Skill speziell fuer den Raw-zu-Wiki-Pfad. |
| Kontextkosten | Wenn beides drin: SKILL.md waechst auf >700 Zeilen, Trigger werden unscharf. | Schmal, weil Single Responsibility. |

Die Outputs, Risiken und Trigger sind **kategorisch unterschiedlich**. Ein gemeinsamer Skill wuerde:

- die Trigger-Description verwaessern (Claude muesste lernen, wann "Blueprint im Chat" vs. "Wiki-Datei schreiben" gemeint ist),
- den Schreib-Hook `wiki-curation-check` mit dem read-only Designer mischen,
- bei jedem Lauf unnoetige Kontextkosten produzieren.

**Konsequenz fuer diesen Skill:**

- `agentic-workflow-designer` bleibt **rein blueprint-orientiert**. Kein Wiki-Schreiben.
- Wenn ein User eine Raw-Datei kuratieren will, gibt der Designer einen Blueprint aus, der **zeigt**, wie der `raw-inbox-curator` das tun wuerde — aber er macht es nicht selbst.
- Der `raw-inbox-curator` wird in einem separaten TODO/Slice gebaut, **nachdem** dieser Designer 2-3 mal real gelaufen ist und der Bedarf bestaetigt wurde (siehe `promotion-log.md`).

**Was wenn der User trotzdem direkt kuratieren will?**

- Designer gibt im Blueprint die Empfehlung: "Naechster Schritt: nutze den noch-nicht-existierenden `raw-inbox-curator` ODER mache es manuell mit folgenden 6 Schritten (siehe `references/workflows.md` Workflow E)."
- Manuell-Pfad ist immer dokumentiert, damit der User nicht blockiert ist.

## D2 — Hooks bleiben read-only

**Datum:** 2026-04-30
**Frage:** Sollen die geplanten Hooks (`raw-write-guard`, `wiki-curation-check`) bei Verstoessen blocken oder nur warnen?

**Entscheidung:** Nur warnen (Read-Only-Checker). Siehe `references/hooks-readonly.md`.

**Begruendung:**

- Blockierende Hooks brauchen ein robustes Override-Konzept, sonst frustrieren sie. Das ist eigene Designarbeit.
- Im V1-Stadium (vor 2-3 realen Laeufen) wissen wir nicht genug, um die Block-Regeln scharf zu schneiden. Falsch-Positive wuerden die Akzeptanz toeten.
- Read-only-Hooks erzeugen **Telemetrie ueber Verstoesse**, ohne den Workflow zu unterbrechen. Aus dieser Telemetrie kann spaeter eine echte Block-Regel werden.

## D3 — Mermaid ist Beilage, nicht Spezifikation

**Datum:** 2026-04-30
**Frage:** Darf der Designer Workflows ausschliesslich als Mermaid-Diagramm liefern?

**Entscheidung:** Nein. Mermaid ist optional, aber **kein Ersatz** fuer den Text-Ablauf.

**Begruendung:**

- Diagramme komprimieren, aber sie verlieren Entscheidungspunkte, Fehlerpfade und Verifikationsschritte.
- Der Output muss von einem Skill-Creator weiterverarbeitbar sein. Mermaid alleine ist dafuer zu unstrukturiert.
- Wenn jemand das Diagramm anders liest als der Autor, gibt es keinen Schiedsrichter. Der Text ist der Schiedsrichter.

## D4 — Promotion-Verdict ist Empfehlung, nicht Aktion

**Datum:** 2026-04-30
**Frage:** Wenn das Verdict `promote` lautet, soll der Skill direkt einen neuen Skill scaffolden?

**Entscheidung:** Nein. Verdict ist Text-Output. Scaffolden ist ein eigener, expliziter Schritt durch den User.

**Begruendung:**

- Trennung von Empfehlung und Aktion erlaubt dem User, vor dem Schreiben noch zu reviewen oder den Vorschlag zu modifizieren.
- Auto-Scaffold wuerde den Designer in einen Executor verwandeln und seine Grenzen verletzen (siehe `SKILL.md` Abschnitt "Grenzen").
- Wenn der User scaffolden will, ist dafuer `skill-creator` (oder das Skillschmiede-Setup) zustaendig.
