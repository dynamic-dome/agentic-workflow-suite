---
name: workflow-design
description: Turn a raw idea, file, or wiki page into a concrete workflow blueprint with Skill/Command/Hook/MCP recommendation
argument-hint: <source — pfad, wiki-link, oder inline-text>
---

# /workflow design

Aktiviert den `agentic-workflow-designer`-Skill mit der Quelle aus `$ARGUMENTS`.

Wenn `$ARGUMENTS` leer ist: frage den User nach einer Quelle (Pfad, Wiki-Link oder Inline-Text in Quotes).

Wenn `$ARGUMENTS` gesetzt ist:

1. Quelle aufloesen (Pfad lesen oder Inline-Text uebernehmen).
2. Privacy-Klasse bestimmen aus Pfad-Prefix (`wiki/raw/` -> privat, `wiki/` -> projekt, `~/Desktop/` -> projekt, URL -> oeffentlich).
3. `agentic-workflow-designer`-Skill mit der Quelle aufrufen.
4. Output ist ein Workflow-Blueprint nach dem Skill-Schema.

**Erwarteter Output:** Markdown-Block mit Quelle, Beobachtung, Ableitung, Workflow, Bauteil-Empfehlung, Promotion-Verdict, Grenzen.
