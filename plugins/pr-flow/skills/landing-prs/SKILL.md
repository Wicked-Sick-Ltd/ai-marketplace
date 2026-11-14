---
name: landing-prs
description: Use when a change is finished and needs to reach a default branch, or when asked to open/raise/create a PR, push and PR, watch/monitor/keep an eye on CI, wait for CI or reviewer/bot comments, check or deal with PR comments, fix review findings, merge (or "merge once green"), check whether a PR merged or anything was missed, ship/land it, or sweep outstanding PRs. Also use before pushing to main/master/develop for any reason. When the work is finished, open the pull request ready for review (no --draft), including Critical-tier changes, or mark an existing draft ready with gh pr ready.
---

# Landing PRs

A change is not done when the tests pass locally. It is done when it is on the
default branch through a pull request whose CI **and reviewer bots** have all
finished and been answered. This skill is that lifecycle; `$pr` is its
command form. Org policy: `Wicked-Sick-Ltd/ai-grok-repo/CONVENTIONS.md`
("Shipping changes") and the Notion page *Repository Standards & Governance*.

**Violating the letter of the lifecycle is violating the spirit of it.**

## Ready for review (Craig, 5 Nov 2026)

When a cloud agent finishes its work, open the pull request ready for review.
Do not pass `--draft`. If a draft already exists, run
`gh pr ready <PR> --repo <OWNER/REPO>` before waiting on reviewers or CI, so
reviewers and CI start straight away.

A draft is only allowed while work is still in progress. That includes
Critical-tier repositories and changes that touch auth, payments, migrations,
infra or secrets. A finished PR left as draft is a red flag.

Done is unchanged. Claude, Bugbot, Copilot, CodeQL and Semgrep have run, every
finding is fixed or answered, every thread is resolved, and CI is green.

## The lifecycle

1. **Branch.** Never commit on `main`/`master`/`develop`. If you are on one,
   `git checkout -b fix/<slug>` (or `feat/`) before committing. Direct pushes
   to a default branch are forbidden even when they would succeed (org owners
   bypass the ruleset silently).
2. **Open.** Push the branch; `gh pr create` against the repo's integration
   branch (`develop` where the repo has a staging flow, else the default
   branch). Body: *Why / Root cause or design / What changed / Verification*,
   honest about what was not verified. When the work is finished, omit
   `--draft`, or run `gh pr ready <PR> --repo <OWNER/REPO>` on an existing
   draft (see **Ready for review**). Pass `--draft` only while work is still
   in progress, including Critical-tier repos.
3. **Wait.** Run `pr-wait.sh <PR>` from this skill's directory (see
   `--help`). It returns only when every check run on the head commit is
   terminal, and on our repos every reviewer bot registers a check run, so that
   is the moment reviews have landed too. "Checks green" before the bots
   finish is not green. Commit statuses are waited on with the check runs and
   count toward the same totals. The default poll is 90s (`--interval` or
   `PR_WAIT_INTERVAL`, minimum 60s). Each poll is one GraphQL query for check
   runs, commit statuses, review threads and mergeability (and the reviews and
   issue comments the digest prints). Before each poll, if fewer than 500
   GraphQL points remain, the script sleeps until the rate-limit reset and logs
   that. Do not poll around it, and do not pass an interval under 60s.
4. **Triage.** For each failed check and each OPEN review thread in the
   digest: reproduce, fix at the root with a test (add a focused regression test), push, and go back to step 3. A
   finding you disagree with gets a reply explaining why, never silence.
   Resolve threads you addressed.
   Review comments from Claude, Bugbot, Copilot, CodeQL and Semgrep all count: every finding is fixed or answered, and every thread is resolved, before the PR counts as done.
5. **Merge** when asked to merge/land/ship, or when running autonomously on a
   non-Critical repo. If the finished PR is still a draft, run
   `gh pr ready <PR> --repo <OWNER/REPO>` first.
   Then `gh pr merge --squash --delete-branch` (rebase where the repo prefers
   it; merge commits are disallowed by the org ruleset). Read
   `merge_state` from the pr-wait SUMMARY (same poll as the checks). If it is
   `BEHIND` (the base moved since the checks ran), `gh pr update-branch` and go
   back to step 3 — checks must pass on the head that merges. `BLOCKED` means a
   rule you cannot satisfy from here: report it. `UNKNOWN` is not settled:
   do not merge on it. Never `--admin` past a refusal.
6. **Deploy** if the repo's `AGENTS.md` names a post-merge step (for example
   `git pull` on a server with an editable install). Then report.

## When the user explicitly orders a direct push

The user's word outranks this skill, but only when it is explicit and
reaffirmed. If the user says to push to a default branch directly: state the
policy in one sentence and ask them to confirm. If they reaffirm, do it, and in
the same turn open a follow-up PR or issue that records the bypass and what
still needs reviewing. Urgency you inferred yourself is not an order.

## Quick reference

| Ask | Do |
|---|---|
| "push and create a PR", "raise the PR" | steps 1–3, ready for review when the work is finished, report the digest |
| "watch CI", "keep an eye on the PR", "wait for comments and fix" | steps 3–4 until clean |
| "merge", "merge once green", "ship it", "land it" | steps 3–6 |
| "did this merge?", "anything missed in the comments?" | `pr-wait.sh --no-wait`, then report |
| "check all outstanding PRs" | `gh pr list`, then this table per PR |

## Rationalisations (all observed, all wrong)

| Excuse | Reality |
|---|---|
| "Small, tested fix — straight to main is fine" | Main pushes skip the bots and hide CI breakage; a 6-hour CI hang went unnoticed for two weeks this way. |
| "Critical-tier work stays a draft so review can wait" | A draft blocks reviewers and CI. Draft only while work is still in progress; a finished PR, Critical tier included, is ready for review. |
| "Local suite is green, so it's done" | Local ≠ CI (different OS, start method, services). CI is the gate. |
| "All checks passed, reporting done" | Reviewer bots post minutes after checks; the digest, not the checks tab, says when you are done. |
| "The bot's comment is a nit" | Reply with the reason. An unanswered thread is an unfinished PR. |
| "I'll deploy now and PR later" | Deploy follows merge. The order is the policy. |

## Red flags

`git push origin main` · reporting before `pr-wait.sh` returned · a digest with
`unresolved_threads>0` in your final message · `gh pr merge --admin` · a finished PR left as draft.

## Grok Build execution

Use this skill in xAI Grok Build (`grok`). Resolve bundled helper paths relative to this `SKILL.md` file. Read repository `AGENTS.md` instructions first. Use connected Notion/MCP tools when available; do not invent tool names.
