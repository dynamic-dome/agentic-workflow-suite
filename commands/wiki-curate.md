---
name: wiki-curate
description: Promote a raw inbox file (image, voice transcript, telegram note) into a curated wiki page
argument-hint: <raw-pfad — datei in wiki/raw/>
---

# /wiki curate

Aktiviert den `raw-inbox-curator`-Skill mit dem Raw-Pfad aus `$ARGUMENTS`.

Wenn `$ARGUMENTS` leer ist: frage nach dem Raw-Pfad.

Wenn `$ARGUMENTS` gesetzt ist:

1. Pfad pruefen — muss in `wiki/raw/` liegen, sonst Fehler.
2. **Privacy-Check:** wenn Quelle als privat markiert (Diary, Telegram-Privat) — Hook `private-export-gate` vorschalten.
3. `raw-inbox-curator`-Skill aufrufen.
4. Output ist eine neue kuratierte Wiki-Seite plus Index-/Log-Updates. Raw-Datei bleibt unveraendert.

**Erwarteter Output:** Pfade der erstellten/geaenderten Dateien, plus Bestaetigung "raw unchanged".
