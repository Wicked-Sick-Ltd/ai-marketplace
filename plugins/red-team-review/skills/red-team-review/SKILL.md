---
name: red-team-review
description: >-
  Use before shipping a claim, public copy, pricing, legal or investor
  statement, launch, cutover or big merge, or when the owner asks for an
  adversarial review, devil's advocate, fact-check or pre-mortem.
---
# Red-team review: adversarial fact-check + pre-mortem

Goal: prove a claim or plan wrong before the world does. The reviewer never wrote the thing under review and never fixes it.

## 1. Frame (2 minutes)
- Write the claim(s) or plan as numbered, testable statements. Vague claims get rewritten until they can be checked, or flagged as unfalsifiable.
- Note the stakes: who sees it, what breaks if it's wrong, and whether it's reversible.

## 2. Adversarial debate (two independent agents or passes)
- **Prosecutor:** assume each statement is FALSE. Build the strongest case: counter-evidence, edge cases, stale data, wrong assumptions, misread sources, overpromising wording.
- **Defender:** assume it is TRUE and gather primary evidence (code, live behaviour, official docs, first-party data). Opinion and our own earlier docs don't count as proof.
- Run them separately so neither anchors on the other. Use agents that didn't author the work.
- **Judge:** for each statement, give one verdict:
  - HOLDS: primary evidence supports it and the prosecutor's best point is answered.
  - FAILS: there's counter-evidence. Give the correction.
  - UNPROVEN: no primary evidence either way. Soften it, remove it, or get the evidence.

## 3. Pre-mortem
- Assume it's 30 days later and this went badly wrong. List the 5-10 most plausible failure stories (technical, factual, legal, brand, customer, cost).
- Rank them by likelihood times impact. For the top 3, give a fix now, a guard or monitor that would catch it early, and a rollback.

## 4. Report (short)
- A verdict table: statement, verdict, evidence link, fix.
- The top pre-mortem risks, each with its guard.
- An overall result: SHIP, SHIP WITH FIXES or HOLD.
- Nothing ships on HOLD. FAILS items go back to the author, not to the reviewer.

## Guardrails
- Cite sources for every verdict, and never invent evidence. Unknown means UNPROVEN.
- Reviewing doesn't widen permissions: the same hold and approval rules apply.
- Scale the effort to the stakes. A typo fix doesn't need a debate; public claims, money, legal, security and irreversible changes do.
- For code, pair this with an independent code review. For multi-slice work, run it as the verify stage of an independent review.
