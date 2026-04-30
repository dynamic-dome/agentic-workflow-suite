---
name: review-fix-verify-loop
description: Use when a code change is risky enough that a linear patch is not safe — separates Review (find findings), Fix (apply minimal patch), and Verify (run tests/lints/UI checks) into distinct phases with feedback. Trigger phrases - "review-fix-verify", "review this patch", "kritischer review", "pruef das nochmal", "patch reviewen", "/review-loop". Each finding requires evidence (file:line, test, screenshot). Skip when the change is trivial or already verified, and skip when there is no test/verification surface (then prefer plain code-reviewer).
---

# Review-Fix-Verify Loop

## Was dieser Skill tut

Trennt einen riskanten Patch in 3 Phasen: **Review** sucht Findings mit Evidenz, **Fix** behebt nur bestaetigte Findings minimal, **Verify** laesst Tests laufen und prueft den Stand. Bei Fehlschlag zurueck zu Review, nicht direkt finalisieren.

## Wann diesen Skill nutzen

- Patch beruehrt heisse Stellen (Auth, Migration, Payment, Race Conditions).
- Tests muessen neu laufen, weil Verhalten sich aendern koennte.
- Findings koennten bestritten werden — Evidenz wird zur Pflicht.
- User will explizite Adversarial-Review-Schritte.

**Nicht nutzen** wenn:

- Aenderung ist trivial (Typo, Doku, Rename eines Identifiers).
- Es gibt keine Test- oder Verifikations-Oberflaeche (`code-reviewer` reicht).
- Aenderung wurde schon verifiziert — dann nur Synthese.

## Ablauf (verbindlich)

### Phase 1: Review

1. **Diff lesen** (`git diff <range>`).
2. **Findings sammeln.** Jeder Finding hat: Datei, Zeile, Klasse (Bug, Risiko, Regression, fehlender Test, Style-Bruch), Evidenz.
3. **Evidenz pflicht.** Behauptung ohne Evidenz ist kein Finding, sondern eine Vermutung — markiere sie als "needs-confirmation", nicht als Finding.
4. **Schwere klassifizieren.** P0 (blocker), P1 (must-fix-before-merge), P2 (sollte gefixt werden), P3 (nice-to-have).

### Phase 2: Fix

1. **Nur bestaetigte Findings beheben.** P0+P1 sind Pflicht, P2 nach Bandbreite, P3 ueberspringen.
2. **Patch minimal halten.** Pro Finding moeglichst eine Zeile / ein Block — kein "Refactor at the same time".
3. **Keine neuen Imports oder API-Aenderungen** ohne explizite Bestaetigung.

### Phase 3: Verify

1. **Tests laufen lassen.** Welche Test-Suite ist relevant? Pflicht.
2. **Lints + Type-Checks.** Wenn vorhanden.
3. **Manuelle Checks.** UI-Test, Smoke-Test, Log-Check, je nach Aenderung.
4. **Bei Fehlschlag:** zurueck zu Phase 1, nicht zu Phase 2.

### Synthese

Pro Run am Ende ein Synthese-Block:

```yaml
synthesis:
  state: ready-to-merge | needs-more-fixes | needs-rescope
  remaining_risk: <konkret>
  next_step: <konkret>
```

## Output-Schema (Pflicht)

```yaml
review_fix_verify:
  scope: <branch oder PR oder file-set>
  phase_1_findings:
    - file:line:
      class:
      severity: P0 | P1 | P2 | P3
      evidence:
      verdict: confirmed | needs-confirmation | dismissed
  phase_2_fixes:
    - finding_ref:
      patch: <pfad+zeile>
      verified: true | false
  phase_3_verification:
    tests:
      ran:
      passed:
      failed:
    lints:
    other_checks:
  synthesis:
    state:
    remaining_risk:
    next_step:
```

## Akzeptanzkriterien

1. Kein Finding ohne Evidenz.
2. Phase 2 hat nur Patches zu Findings aus Phase 1.
3. Phase 3 hat eine Test-Liste und ein Pass/Fail-Ergebnis (kein "vermutlich okay").
4. Synthese benennt entweder ready-to-merge oder einen konkreten naechsten Schritt.
5. Bei Phase-3-Failure war es zurueck zu Phase 1, nicht direkt finalisieren.

## Grenzen

- **Macht keine Architektur-Aenderungen.** Bei "Findings die einen Refactor brauchen" -> zurueck zum User mit Rescope-Vorschlag.
- **Verlaesst sich nicht auf Self-Reflection.** Tests, Greps, Lints — externe Evidenz.
- **Single-Repo.** Multi-Repo-Reviews -> `dynamic-graph-auditor` davorschalten.

## Naming-Collision-Hinweis

`devil-advocate-swarms` macht Multi-Agent-Adversarial-Review (Scanner -> Debate -> Consensus -> Fix). Dieser Skill ist single-loop und kleiner. Bei sehr breiten Sicherheits-Reviews lieber das Plugin nutzen.
