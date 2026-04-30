---
name: skill-promote
description: Check whether a recurring pattern should become a real Skill (promote / keep-as-pattern / already-covered / reject)
argument-hint: <pattern-name oder pattern-pfad>
---

# /skill promote

Aktiviert den `skill-promotion-checker`-Skill mit dem Pattern aus `$ARGUMENTS`.

Wenn `$ARGUMENTS` leer ist: frage nach dem Pattern (Name, Wiki-Pfad zur Pattern-Seite oder Beschreibung).

Wenn `$ARGUMENTS` gesetzt ist:

1. Pattern-Beschreibung aufloesen (Wiki-Page lesen oder User-Beschreibung uebernehmen).
2. Naming-Collision-Lookup gegen `~/.claude/skills/` und installierte Plugins.
3. `skill-promotion-checker` mit den 6 Checks anwenden.
4. Verdict ausgeben — **kein** automatisches Scaffold.

**Erwarteter Output:** YAML-Block mit `verdict`, `reason`, `checks`, `naming_collision`, `next_step`.
