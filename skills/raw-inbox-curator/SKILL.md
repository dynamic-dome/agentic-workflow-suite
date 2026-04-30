---
name: raw-inbox-curator
description: Use when raw inbox material (image, voice transcript, telegram note, link) in wiki/raw/ should be promoted into a curated wiki page with proper frontmatter, sources, and cross-links. Trigger phrases - "curate this raw file", "promote raw to wiki", "kuratiere die raw datei", "ins wiki ueberfuehren", "raw inbox aufraeumen", "/wiki curate". The skill writes a NEW wiki page; the raw file stays untouched. Skip when the user wants only to read raw content without producing a wiki artifact, or when the source is not in wiki/raw/.
---

# Raw-Inbox Curator

## Was dieser Skill tut

Ueberfuehrt Material aus `wiki/raw/` in eine kuratierte Wiki-Seite. Output: eine neue Datei in `wiki/concepts/`, `wiki/patterns/`, `wiki/queries/`, `wiki/sources/` oder `wiki/todos/` (je nach Inhalt) plus Updates in `wiki/index.md` und `wiki/log.md`.

## Wann diesen Skill nutzen

- Datei in `wiki/raw/` (Bild, MD, Voice-Transkript) soll ins kuratierte Wiki.
- User sagt explizit "kuratiere", "ins wiki", "promote raw".

**Nicht nutzen** wenn:

- Quelle ist nicht in `wiki/raw/`.
- User will nur lesen, nicht persistieren.
- Inhalt ist privat (Diary, Telegram-Privat) — dann erst `private-export-gate`-Hook konsultieren.

## Ablauf (verbindlich)

1. **Raw-Datei lesen oder visuell pruefen.** Pfad explizit zitieren.
2. **Beobachtung extrahieren.** Bei Bildern: sichtbare Elemente. Bei Text: Schluesselbegriffe. **Beobachtung != Interpretation**.
3. **Ableitung formulieren.** Was bedeutet das, getrennt von der Beobachtung.
4. **Wiki-Klasse bestimmen.** `concept` (Wissen), `pattern` (Ablauf), `query` (Frage), `source` (externe Quelle), `todo` (Auftrag).
5. **Kuratierte Seite schreiben.** Frontmatter mit `type`, `status`, `tags`, `applies_to`, `source` (Pfad zur Raw-Datei). Mindestens "Beobachtung", "Ableitung" und "Quellen"-Sektionen.
6. **Index und Log aktualisieren.** `wiki/index.md` bekommt einen Eintrag, `wiki/log.md` eine Zeile mit Datum.
7. **Raw-Datei NICHT veraendern.** Nur lesen, nie schreiben/verschieben.

## Output

Drei Dateien aendern, eine schreiben:

```yaml
created:
  - wiki/<klasse>/YYYY-MM-DD-<slug>.md
modified:
  - wiki/index.md   # neuer Eintrag
  - wiki/log.md     # eine Zeile
unchanged:
  - <raw-pfad>      # explizit erwaehnen, dass nicht angefasst
```

## Pflicht-Frontmatter der neuen Seite

```yaml
type: concept | pattern | query | source | todo
status: seed | active
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [...]
source: <raw-pfad>
applies_to: [...]
```

## Akzeptanzkriterien

1. Raw-Pfad ist in der neuen Seite zitiert.
2. Beobachtung und Ableitung sind als getrennte Sektionen sichtbar.
3. Frontmatter hat alle Pflichtfelder (`type`, `status`, `created`, `tags`, `source`).
4. `wiki/index.md` enthaelt einen neuen Link.
5. `wiki/log.md` hat eine Zeile mit dem heutigen Datum.
6. Raw-Datei ist unveraendert.

## Grenzen

- **Schreibt nicht in `raw/`.** Wenn versucht wird, blockt `raw-write-guard`-Hook.
- **Macht keine Privacy-Entscheidung.** Bei privaten Quellen Hook `private-export-gate` auf Bestaetigung warten lassen.
- **Promoted nicht automatisch zu pattern/concept.** Erst `seed`, spaeter Upgrade nach Review.

## Naming-Collision-Hinweis

Existierender Skill `obsidian-sync` (in `agentic-os`) deckt verwandte Funktionen ab — fokussiert auf Session-Wiki-Sync, **nicht** Raw-Inbox-Kuratierung. Beide koexistieren absichtlich.
