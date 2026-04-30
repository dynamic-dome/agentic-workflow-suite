# Workflow-Archetypen (Referenz)

Verwendet von `agentic-workflow-designer`, Schritt 2 (Workflow-Typ routen).

Jeder Archetyp hat: **Zweck**, **Wann nutzen**, **Ablauf**, **Skill-Kandidat**.
Wenn keiner passt, baue einen neuen Workflow und begruende es im Blueprint.

---

## A. Intake Router

**Zweck:** Jede Anfrage zuerst in den passenden Arbeitsmodus routen.

**Wann nutzen:** Mehrdeutiger Input — User sagt "mach daraus", "baue", "review", aber Modus unklar.

**Ablauf:**
1. Input-Typ bestimmen: Code, Wiki, Raw-Inbox, Bild, Planung, Security, DCO/MCP.
2. Ziel bestimmen: Antwort, Datei, Wiki-Seite, Code-Patch, Skill-Blueprint, echter Skill.
3. Risiko bestimmen: read-only, write, privacy, security, external tool, irreversible.
4. Naechsten Workflow waehlen (B-G).
5. Akzeptanzkriterien notieren.

**Skill-Kandidat:** `workflow-router`.

---

## B. Single Loop Implementation

**Zweck:** Kleine bis mittlere Aufgabe end-to-end mit einer Instanz erledigen.

**Wann nutzen:** Aufgabe passt in einen Kontext, kein Multi-Agent noetig.

**Ablauf:**
1. Kontext lesen.
2. Mini-Plan mit 2-5 Schritten machen.
3. Aenderung umsetzen.
4. Verifikation ausfuehren.
5. Bei Fail: Fehlerursache bestimmen und gezielt neu planen.
6. Final mit geaenderten Dateien, Checks und offenen Risiken.

**Skill-Kandidat:** `single-loop-implementer`.

**Anti-Pattern:** Auf Multi-Agent aufblaehen, solange eine Instanz den Kontext sicher haelt.

---

## C. Dynamic Graph Audit

**Zweck:** Breite Analyse, bei der der genaue Graph erst durch Exploration sichtbar wird.

**Wann nutzen:** Plugin-Oekosystem, Wiki-Struktur, DCO-Funktionslandschaft, Skill-/Hook-/Command-Inventar.

**Ablauf:**
1. Inventar erstellen.
2. Cluster bilden: Zweck, Runtime-Rolle, Datenfluss, Qualitaet, Redundanz.
3. Pro Cluster Audit-Schema anwenden.
4. Querverbindungen markieren.
5. Redundanzen und Synergien ableiten.
6. Ergebnis als Report + Graph + TODOs sichern.

**Skill-Kandidat:** `dynamic-graph-auditor`.

---

## D. Review-Fix-Verify Loop

**Zweck:** Riskante Codeaenderungen nicht als linearen Patch behandeln.

**Wann nutzen:** Patch beruehrt heisse Stellen, Tests muessen neu laufen, Findings koennten bestritten werden.

**Ablauf:**
1. Lead baut oder beschreibt Loesung.
2. Reviewer sucht konkrete Findings (Datei/Zeile/Testbezug).
3. Fixer behebt nur bestaetigte Findings mit kleinem Patch.
4. Verifier laesst Tests/Lints/Greps/UI-Checks laufen.
5. Bei Fail zurueck zu Reviewer/Fixer, nicht direkt finalisieren.
6. Synthese: Zustand, Rest-Risiko, naechster Schritt.

**Skill-Kandidat:** `review-fix-verify-loop`.

**Optionaler Command:** `/review-loop <scope>`.

---

## E. Raw-Inbox to Wiki

**Zweck:** Bilder, Voice-Transkripte, Telegram-Notizen oder Links aus der Raw-Inbox in kuratierte Wiki-Artefakte ueberfuehren.

**Wann nutzen:** Material liegt in `wiki/raw/` und soll in `wiki/` promoted werden.

**Ablauf:**
1. Raw-Datei lesen oder visuell pruefen.
2. Beobachtung extrahieren, ohne Interpretation zu vermischen.
3. Ableitung als Konzept, Pattern, Query, Source oder Todo einordnen.
4. Kuratierte Seite mit Frontmatter, Quellen, Links und Grenzen schreiben.
5. `index.md` und `log.md` aktualisieren.
6. Raw-Datei unveraendert lassen.

**Skill-Kandidat:** `raw-inbox-curator` (oder Referenzmodus dieses Skills — siehe `references/decisions.md`).

**Akzeptanz:**
- Raw-Pfad ist genannt.
- Quellenstatus ist klar.
- Keine Auto-Promotion privater Inhalte.
- Wiki-Link ist im Index auffindbar.

---

## F. DCO Tool-Safe Execution

**Zweck:** DCO-/MCP-/Telegram-/Mini-App-Arbeit mit Tool-Grenzen betreiben.

**Wann nutzen:** Aktion beruehrt externe Tools (DB, MCP, Web/API) und kann Privacy-Klassen ueberschreiten.

**Ablauf:**
1. Intent routen: Chat, Mini App, Telegram, Schedule, MCP.
2. Datenschutzklasse bestimmen: privat, projektbezogen, oeffentlich, operational.
3. Toolbedarf klaeren: lokal, Datei, DB, MCP, Web/API.
4. Tool-Ausgabe validieren.
5. Aktion erst nach Validierung in Wiki/DB/Antwort uebernehmen.
6. Private Quellen nur nach explizitem Export in Wiki oder NotebookLM bringen.

**Skill-Kandidat:** `dco-tool-safe-runner`.

**Hook-Kandidaten:** `raw-write-guard`, `private-export-gate`, `mcp-output-envelope`.

---

## G. Skill Promotion

**Zweck:** Entscheiden, ob ein Workflow ein echter Skill werden soll.

**Wann nutzen:** Workflow ist 3+ mal gelaufen oder riskant genug fuer Codification.

**Ablauf:**
1. Wiederholung pruefen: 3+ mal gebraucht oder hohes Risiko?
2. Stabilitaet pruefen: Trigger, Inputs, Schritte, Outputs klar?
3. Kontextkosten pruefen: SKILL.md unter ~500 Zeilen moeglich?
4. Ressourcen trennen: Kern in `SKILL.md`, Details in `references/`, deterministische Logik in `scripts/`.
5. Skill-Frontmatter schreiben: `name`, `description` mit klaren Triggern.
6. Minimalbeispiel testen.
7. Erst danach in Runtime promoten.

**Skill-Kandidat:** `skill-promotion-checker`.

**Output:**

```yaml
skill_promotion:
  verdict: promote | keep-as-pattern | reject
  reason: "..."
  proposed_name: "..."
  trigger_description: "..."
  required_resources:
    - SKILL.md
    - references/...
    - scripts/...
```

---

## Routing-Hilfe

Wenn unklar, welcher Archetyp passt:

| Symptom im Input | Wahrscheinlicher Archetyp |
|---|---|
| "Was soll ich damit machen?" | A (Intake-Router) |
| "Bau das" + klare Aufgabe | B (Single-Loop) |
| "Schau dir alles an" / "Inventur" | C (Dynamic-Graph-Audit) |
| "Pruef das nochmal" / "Patch reviewen" | D (Review-Fix-Verify) |
| Datei in `wiki/raw/` | E (Raw-to-Wiki) |
| MCP-/DCO-/Telegram-/DB-Aktion | F (DCO-Tool-Safe) |
| "Ist das ein Skill?" | G (Skill-Promotion) |
