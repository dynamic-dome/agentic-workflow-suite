---
name: review-loop
description: Run Review-Fix-Verify on a code change with separated phases and evidence requirement
argument-hint: <scope — branch, PR, oder file-set>
---

# /review-loop

Aktiviert den `review-fix-verify-loop`-Skill mit dem Scope aus `$ARGUMENTS`.

Wenn `$ARGUMENTS` leer ist: frage nach dem Scope (Branch-Name, PR-Nummer oder Datei-Liste).

Wenn `$ARGUMENTS` gesetzt ist:

1. Scope aufloesen (`git diff <range>` oder `gh pr view <num>`).
2. `review-fix-verify-loop`-Skill mit Phase 1 starten.
3. Bei Phase-3-Failure: zurueck zu Phase 1, **nicht** finalisieren.
4. Synthese am Ende mit `state: ready-to-merge | needs-more-fixes | needs-rescope`.

**Erwarteter Output:** YAML-Block mit Findings, Fixes, Verifikation und Synthese.
