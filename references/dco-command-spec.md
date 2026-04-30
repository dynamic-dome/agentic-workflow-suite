# DCO-Command-Spec: `/workflow design <source>`

**Status:** Spezifikation, nicht implementiert. Soll im DCO (Dynamic Central Orchestrator) als Mini-App-/Chat-Command verfuegbar werden.

## Zweck

Ein User-facing Trigger im DCO, der den `agentic-workflow-designer` Skill startet — egal ob die Quelle eine lokale Datei, eine Wiki-Seite, ein Bild aus der Raw-Inbox oder eine inline beschriebene Idee ist.

## Signatur

```text
/workflow design <source>
```

`<source>` kann sein:

| Form | Beispiel | Aufloesung |
|---|---|---|
| Wiki-Pfad | `wiki/raw/2026-04-30-whiteboard.jpg` | Datei lesen, an Designer geben |
| Wiki-Page-Alias | `[[wiki/concepts/agentic-loop]]` | Wiki-Resolve, Inhalt an Designer geben |
| Lokaler Pfad | `~/Desktop/Sketch/idea.txt` | Datei lesen, **nur** wenn innerhalb User-Home |
| Telegram-Reply | `<reply auf eine Nachricht mit Bild/Voice>` | Reply-Inhalt holen, an Designer geben |
| Inline-Text | `/workflow design "ich will eine pipeline die ..."` | Text als Quelle nehmen |
| URL | `/workflow design https://...` | URL fetchen, **nur** wenn `firecrawl` MCP verfuegbar |

## Argument-Parsing

1. Erste Form pruefen: Pfad, URL oder Quotes-Text.
2. Bei mehrdeutiger Eingabe ohne Quotes: nachfragen, **nicht** raten.
3. Wenn Quelle nicht aufloesbar: klare Fehlermeldung mit erkanntem Typ und vermuteter Ursache.

## Backend-Routing

```text
DCO-Command-Handler
  -> Source-Resolver (gibt Markdown + Privacy-Klasse zurueck)
  -> agentic-workflow-designer Skill
  -> Output-Renderer (zeigt Blueprint im Chat / Mini-App)
```

**Source-Resolver** ist die kritische Stelle:

- Liest die Quelle.
- Bestimmt Privacy-Klasse aus Pfad-Prefix:
  - `wiki/raw/` -> privat
  - `wiki/` -> projekt
  - `~/Desktop/` -> projekt (nicht oeffentlich)
  - URL -> oeffentlich (annahme)
- Liefert ein Envelope `{markdown_content, source_path, privacy_class, source_kind}`.

## Privacy-Grenzen (hart)

1. **Keine Auto-Promotion.** Auch wenn der Blueprint sagt `promote` — kein Skill wird automatisch erzeugt.
2. **Raw-Pfade sind read-only.** Source-Resolver oeffnet sie mit `read`, niemals mit `write` oder `move`.
3. **Privates wird nicht extern geteilt.** Wenn `privacy_class == privat` und ein Tool die Quelle nach aussen senden wuerde (z. B. NotebookLM-Upload, externe API), Block mit Warnung.
4. **Audit-Logs.** Jeder Lauf laesst eine Zeile in `dco/logs/workflow-design.ndjson` mit `timestamp`, `source_path`, `privacy_class`, `verdict`. Kein Quell-Inhalt im Log.

## Output-Channels

- **Chat:** Blueprint als Markdown-Block. Bei langen Outputs: Truncation mit "Vollversion in Mini-App ansehen"-Link.
- **Mini-App:** Blueprint formatiert mit Sektionen, Copy-Buttons fuer `name`/`description`-Vorschlaege.
- **Telegram:** Kurzfassung (Workflow-Name + Verdict + Link zur Mini-App). Voll-Output nicht inline, weil zu lang.

## Beispiele

### Beispiel 1 — Wiki-Raw

```text
User: /workflow design wiki/raw/2026-04-30-whiteboard.jpg
DCO: Pruefe Quelle... Bild gefunden, privat. Designer-Skill startet.
DCO: <Blueprint im Chat>
```

### Beispiel 2 — Inline

```text
User: /workflow design "wenn telegram-voice rein kommt, transkribieren und ins wiki"
DCO: Inline-Quelle erkannt (109 Zeichen). Designer-Skill startet.
DCO: <Blueprint im Chat>
```

### Beispiel 3 — URL ohne Firecrawl

```text
User: /workflow design https://blog.example.com/agent-patterns
DCO: URL-Quelle erkannt, firecrawl MCP nicht verfuegbar. Abbruch.
     Tipp: Inhalt als Inline-Quelle einfuegen oder firecrawl aktivieren.
```

## Fehlermodi

| Fehler | Ursache | Aktion |
|---|---|---|
| `source-not-found` | Pfad existiert nicht | klare Fehlermeldung mit erkanntem Typ |
| `permission-denied` | Pfad ausserhalb erlaubter Roots | Block, mit Hinweis auf erlaubte Roots |
| `parse-ambiguous` | Eingabe ist weder klarer Pfad noch Quote | Rueckfrage, nicht raten |
| `privacy-export-blocked` | Tool wuerde private Quelle nach aussen senden | Block mit Erklaerung |
| `designer-output-incomplete` | Skill hat Pflicht-Block leer gelassen | Output zurueckweisen, Skill nochmal laufen lassen |

## Implementierungs-Reihenfolge

1. Source-Resolver isoliert bauen und testen (Inline + Wiki-Pfad reichen).
2. DCO-Command-Handler dranschalten.
3. Output im Chat-Channel zeigen.
4. Mini-App-Renderer erst nach 2-3 erfolgreichen Chat-Laeufen nachziehen.
5. Telegram-Adapter ganz am Schluss, weil Truncation-Logik komplex ist.

## Was diese Spec NICHT ist

- Keine Code-Implementierung. Nur Interface-Vertrag.
- Keine Auto-Schedule-Routine. Wenn der User Workflows periodisch designen will, ist das ein eigenes Feature.
- Keine Multi-User-Konflikte abgedeckt. DCO ist single-user, das reicht fuer V1.
