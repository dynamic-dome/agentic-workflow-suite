# Promotion-Checks (Referenz)

Verwendet von `agentic-workflow-designer`, Schritt 5 (Promotion-Check).

Ein Workflow wird zum Skill **nur** wenn folgende Checks alle gruen sind. Anderenfalls bleibt er Pattern oder wird verworfen.

## Checkliste

| # | Check | Frage | Schwelle |
|---|---|---|---|
| 1 | Wiederholung | Wurde der Ablauf 3+ mal gebraucht oder ist er riskant genug? | 3 dokumentierte Laeufe ODER hohes Risiko (Privacy, Datenverlust, externe Aktion) |
| 2 | Trigger-Klarheit | Sind die Trigger-Phrasen so spezifisch, dass Claude den Skill zuverlaessig feuert und nicht overtriggered? | Mindestens 3 konkrete Trigger-Phrasen + 1 Anti-Trigger |
| 3 | Stabilitaet | Sind Inputs, Schritte, Outputs ueber die letzten Laeufe konstant? | Kein wesentlicher Schritt hat sich in den letzten 2 Laeufen geaendert |
| 4 | Kontextkosten | Kann `SKILL.md` unter ~500 Zeilen bleiben (mit `references/` fuer Tiefe)? | Ja, mit klarer Trennung Kern vs. Referenz |
| 5 | Testbarkeit | Gibt es ein Minimalbeispiel, an dem man den Skill verifizieren kann? | Mindestens 1 Beispiel-Input mit erwartetem Output |
| 6 | Rollback | Wenn der Skill falsch laeuft, kann man die Aenderung leicht rueckgaengig machen? | Skill schreibt nicht in irreversible Stellen ohne Bestaetigung |

## Verdict-Matrix

- **promote** — alle 6 Checks gruen, kein bestehender Skill deckt es ab.
- **keep-as-pattern** — Checks 1-4 gruen, aber 5 oder 6 fehlen. Workflow ist gut, aber als Skill noch nicht reif. Im Wiki als Pattern halten.
- **already-covered** — Checks waeren erfuellbar, aber ein bestehender Skill / Plugin / Standard-Tool deckt das Thema bereits ab. Codification waere Duplikat. Aktion: Backlink ziehen, ggf. den existierenden Skill ergaenzen oder umbenennen, **kein** neuer Skill. Erkannt via Naming-Collision-Check (siehe SKILL.md Schritt 4).
- **reject** — einer der Checks 1-3 ist rot. Der Workflow ist nicht stabil oder zu nischig. Nicht codifizieren.

## Anti-Patterns (sofort `keep-as-pattern` oder `reject`)

- Skill macht alles und alles "ein bisschen". Trigger ist generisch ("automate things").
- Skill duzpliziert einen bestehenden Skill mit minimalen Abweichungen.
- Skill braucht laufende Pflege weil sich das zugrundeliegende Tool monatlich aendert.
- Skill schreibt direkt in Production-DBs oder externe APIs ohne expliziten Bestaetigungsschritt.
- Skill kann nur von einer einzigen Person reproduziert werden (impliziter Kontext).

## Reason-Vorlagen

Wenn `verdict: promote`:

> "Workflow ist N mal gelaufen mit stabilen Schritten. Trigger sind eindeutig. SKILL.md kann unter X Zeilen bleiben. Risiko: <…>. Naechster Schritt: scaffolden via skill-creator."

Wenn `verdict: keep-as-pattern`:

> "Workflow ist nuetzlich, aber Check #<N> fehlt: <warum>. Vorschlag: noch <bedingung> abwarten, dann erneut pruefen."

Wenn `verdict: already-covered`:

> "Workflow ist promotionsreif, aber `<existing-skill-or-plugin>` deckt das Feld bereits ab (Match: <name | trigger | scope>). Stattdessen: Backlink in `<source-page>` auf `<existing>` ziehen ODER `<existing>` um <feature> erweitern. Kein neuer Skill noetig."

Wenn `verdict: reject`:

> "Workflow ist zu <generisch | instabil | nischig>. Codifizieren wuerde mehr Wartung als Nutzen erzeugen. Stattdessen: <alternative>."
