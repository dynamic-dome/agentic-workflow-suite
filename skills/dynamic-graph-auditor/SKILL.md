---
name: dynamic-graph-auditor
description: Use when a broad ecosystem (plugin landscape, wiki cluster, repo monorepo, DCO function map) needs an audit where the actual graph emerges through exploration, not from a pre-defined plan. Trigger phrases - "audit the plugin ecosystem", "schau dir alles an", "inventur machen", "find redundancies", "map the wiki", "/workflow audit", "ecosystem review". Returns inventory, clusters, role/dataflow map, redundancies, synergies, prioritized TODOs. Skip when the scope is small enough for a single-loop pass or when the audit was just done within the last 7 days.
---

# Dynamic Graph Auditor

## Was dieser Skill tut

Inventarisiert ein breites Oekosystem und analysiert es als dynamischen Graph — Knoten und Kanten entstehen waehrend der Arbeit, nicht aus einem Voraus-Plan. Output: Report mit Inventar, Clustern, Rollen-/Datenfluss-Map, Redundanz-Liste, Synergie-Vorschlaegen und priorisierten TODOs.

## Wann diesen Skill nutzen

- Plugin-Oekosystem prueft auf Drift, Redundanz, fehlende Manifeste.
- Wiki-Cluster reviewen (welche Konzepte sind veraltet, welche fehlen).
- Repo-Sammlung inventarisieren (welche Repos sind aktiv, welche archive).
- DCO-Funktionslandschaft kartographieren.

**Nicht nutzen** wenn:

- Scope ist klein genug fuer einen einzelnen Lese-Lauf (Single-Loop reicht).
- Audit wurde in den letzten 7 Tagen gemacht — dann lieber Diff seit letztem Audit.
- Aufgabe ist Patch oder Fix — Audit waere Overkill.

## Ablauf (verbindlich)

1. **Scope bestimmen.** Repo-Wurzel, Verzeichnis-Glob oder explizite Datei-Liste.
2. **Inventar erstellen.** Glob aller relevanten Files, Listing in flacher Tabelle (Pfad, Typ, Status, Letztes-Update).
3. **Cluster bilden.** Gruppieren nach: Zweck, Runtime-Rolle, Datenfluss, Qualitaet, Redundanz-Verdacht.
4. **Pro Cluster ein Audit-Schema anwenden.** Manifest-Validitaet, Frontmatter-Konsistenz, Cross-Refs, Versions-Drift, Deprecation-Markers.
5. **Querverbindungen markieren.** Welcher Knoten haengt von welchem ab? Welche sind verwaist?
6. **Redundanzen und Synergien ableiten.** Gleicher Trigger doppelt? Ungenutzte Faehigkeit?
7. **Priorisierte TODO-Liste.** Pro Befund: Severity (P0-P3), konkrete Aktion, Aufwand-Schaetzung.

## Output-Schema (Pflicht)

```yaml
audit:
  scope: <pfad oder beschreibung>
  date: YYYY-MM-DD
  inventory_count: <zahl>

  clusters:
    - name:
      members: []
      role:
      health: green | yellow | red

  role_dataflow:
    - from: <knoten>
      to: <knoten>
      kind: depends_on | supports | applies_to | unknown

  redundancies:
    - description:
      members: []
      proposal:

  synergies:
    - description:
      proposal:

  todos:
    - severity: P0 | P1 | P2 | P3
      action:
      effort: small | medium | large
      target: <pfad oder komponente>
```

Optionaler Ergaenzungsblock: Mermaid-Diagramm des Cluster-Graphs (nur als Visualisierung, nicht als Spec).

## Akzeptanzkriterien

1. Inventar ist vollstaendig (kein "ich habe nicht alles gelesen").
2. Jeder Cluster hat eine `health`-Markierung mit Begruendung.
3. Mindestens eine Redundanz oder Synergie ist genannt (sonst Audit-Wert fragwuerdig).
4. TODOs sind priorisiert, nicht nur aufgelistet.
5. Querverbindungen sind explizit (nicht "es haengt alles irgendwie zusammen").

## Grenzen

- **Macht keine Code-Aenderungen.** Audit liefert TODOs, andere Skills setzen um.
- **Bewertet nicht inhaltlich.** ("Ist Plugin X gut geschrieben?" -> nein, das ist `code-reviewer`-Job.)
- **Skaliert nicht beliebig.** Bei >500 Files: Sampling vorschlagen statt alles lesen.

## Naming-Collision-Hinweis

`agent-orchestrator-plugin` und `multi-model-orchestrator` decken Multi-Agent-Audits ab; dieser Skill ist single-loop und fokussiert auf statische Inventur. Bei sehr grossen Scopes auf Multi-Agent uebergeben.
