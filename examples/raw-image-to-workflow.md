# Beispiel: Raw-Bild zu Workflow zu Skill-Blueprint

Dieses Beispiel zeigt einen kompletten Lauf des `agentic-workflow-designer` an einem konkreten Input. Es dient als **Goldstandard fuer Output-Qualitaet** und als Test-Fall.

## Eingabe

Der User legt diese Datei auf den Tisch:

- **Pfad:** `wiki/raw/2026-04-30-whiteboard-recherche-pipeline.jpg`
- **Beschreibung:** Foto eines Whiteboards mit Pfeilen zwischen den Knoten "Telegram-Voice", "Transcript", "Web-Search", "NotebookLM", "Synthese", "Wiki-Page". Drei Sticky-Notes: "max 5 min Audio", "Quellen muss zitierbar bleiben", "kein Auto-Push ins Wiki".
- **User-Prompt:** "mach daraus einen workflow"

## Lauf

### Schritt 1 — Quelle lesen

**Beobachtung (was steht da):**
- Knoten in dieser Reihenfolge (linksoberes Eck im Uhrzeigersinn): `Telegram-Voice → Transcript → Web-Search → NotebookLM → Synthese → Wiki-Page`.
- 3 Sticky-Notes als Constraints.
- Pfeil von `NotebookLM` zurueck zu `Web-Search` (Loop).
- Kein Pfeil von `Wiki-Page` weiter; Wiki ist Endknoten.

**Interpretation kommt erst in Schritt 3 — nicht vermischen.**

### Schritt 2 — Workflow-Typ routen

Aus `references/workflows.md`: passend ist **E. Raw-Inbox to Wiki**, weil Input in `wiki/raw/` liegt und Output ein Wiki-Artefakt ist.

Aber: der Loop `NotebookLM → Web-Search` ist nicht im E-Standard. Das ist **eine Variante mit Recherche-Loop**. Im Blueprint markieren.

### Schritt 3 — Blueprint schreiben

```markdown
# Workflow-Blueprint: Voice-zu-Wiki-Recherche

## Quelle
- Pfad: wiki/raw/2026-04-30-whiteboard-recherche-pipeline.jpg
- Quellenklasse: raw
- Privacy: privat (Whiteboard-Foto, nicht oeffentlich gedacht)

## Beobachtung
6 Knoten in Pipeline-Form, 1 Loop NotebookLM->Web-Search,
3 Constraints (Audiolaenge, Zitierbarkeit, kein Auto-Push).

## Ableitung
Der User skizziert einen Voice-Note-zu-Wiki-Pipeline-Prozess
mit Recherche-Loop und harten Privacy/Quality-Gates.
Das ist Workflow-Typ E (Raw-to-Wiki) mit Recherche-Variante.

## Workflow
- Trigger: Telegram-Voice-Note > 30 Sekunden landet in raw-inbox.
- Inputs: Audiodatei, Datum, optionale Tags.
- Rollen: 1) Transcriber, 2) Recherche-Agent, 3) Synthesizer, 4) Wiki-Author.
- Ablauf:
  1. Voice-Note transkribieren (max 5 min Cap).
  2. Schluesselbegriffe extrahieren.
  3. Web-Search auf 3-5 Quellen.
  4. Quellen in NotebookLM laden, befragen.
  5. Wenn NotebookLM-Antwort Luecken zeigt: zurueck zu Web-Search (max 2 Iterationen).
  6. Synthese als Markdown-Draft.
  7. Wiki-Page-Vorschlag im Chat zeigen — KEIN Auto-Push.
  8. User bestaetigt explizit, dann erst nach wiki/ schreiben.
- Entscheidungspunkte:
  - Audio > 5 min? -> Abbruch mit Hinweis.
  - Quelle nicht zitierbar? -> Quelle markieren, nicht in Synthese mischen.
- Verifikation:
  - Transcript laenge plausibel.
  - Mind. 3 zitierbare Quellen.
  - Synthese referenziert mindestens 2 Quellen explizit.
- Fehlerpfade:
  - Transkription scheitert -> Audiodatei behalten, User informieren.
  - NotebookLM offline -> auf Web-Search-only-Modus zurueckfallen.
  - User stoppt -> Draft als wiki/raw/ ablegen, nicht promoten.

## Bauteil-Empfehlung
- Ebene: Skill (mit zwei MCP-Contracts: NotebookLM und Web-Search).
- Begruendung (1 Satz): Ablauf wiederholt sich strukturiert
  und braucht zwei externe Faehigkeiten — passt zu Skill + MCP.
- Wenn Skill:
  - name: voice-to-wiki-research
  - description: "Use when a Telegram voice note in wiki/raw/
    needs to become a researched Wiki page with cited sources.
    Triggers: 'voice ins wiki', 'transkribiere und recherchiere',
    'voice-note pipeline'. Skip when the user wants the
    transcript only, without research."

## Promotion
- Verdict: keep-as-pattern
- Reason: Wiederholung-Check noch nicht erfuellt — der User
  hat den Ablauf erst skizziert, nicht 3 mal real laufen lassen.
  Trigger-Klarheit und Stabilitaet sind dagegen schon gegeben.
- Naechster Schritt: 2 reale Laeufe dokumentieren (Voice-Note + Wiki-Output),
  dann erneut Promotion-Check.

## Grenzen
- Macht keine Audio-Bearbeitung jenseits Transkription.
- Pusht nichts automatisch ins Wiki — User muss bestaetigen.
- Loop NotebookLM<->Web-Search ist auf 2 Iterationen gekappt,
  damit der Skill nicht endlos laeuft.
```

### Schritt 6 — Grenzen markieren

Privacy-Hinweis: das Whiteboard-Foto ist privat. **Raw-Datei nicht mutieren**, nur referenzieren. Kein Auto-Promote in `wiki/`.

## Was dieses Beispiel zeigt

1. **Beobachtung kommt vor Interpretation.** Die Reihenfolge der Knoten ist Fakt; die Bedeutung "Voice-zu-Wiki-Pipeline" ist Ableitung.
2. **Constraints aus Sticky-Notes werden ernst genommen.** "Kein Auto-Push" wandert direkt in Schritt 7-8 des Workflows.
3. **Workflow-Typ + Variante.** Der Standard-Archetyp E reicht nicht; die Recherche-Loop wird explizit als Variante markiert.
4. **Promotion-Verdict ist `keep-as-pattern`, nicht `promote`.** Der Skill zeigt damit, dass er ehrlich ist — drei Laeufe bevor codifiziert wird.
5. **Output ist sofort weiterverarbeitbar.** Wenn der User spaeter sagt "ok, jetzt promoten", kann ein Skill-Creator den `name` und die `description` direkt uebernehmen.

## Anti-Beispiel (was dieser Skill NICHT tut)

Falsch waere:

- Direkt `voice-to-wiki-research/SKILL.md` schreiben — der Skill ist Designer, nicht Executor.
- Die Whiteboard-JPG umbenennen oder in `wiki/concepts/` schieben — Raw-Dateien nicht mutieren.
- "Trigger: jede Voice-Note" — zu generisch, wuerde overtriggern.
- Mermaid statt Text-Workflow — Mermaid ist Beilage, kein Ersatz.
