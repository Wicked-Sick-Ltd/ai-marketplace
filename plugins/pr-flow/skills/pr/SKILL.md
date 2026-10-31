---
name: pr
description: "Pull-request lifecycle \u2014 create | watch | merge | land | status | sweep. Waits for CI and every reviewer bot, triages and fixes findings, merges by the repo's rules."
---

You are running the pull-request lifecycle. **REQUIRED SKILL:** read and follow
`landing-prs` (this plugin) — it holds the rules; this command only routes.

RUN CONFIG from the user's arguments for this skill:
- VERB: the first word (`create`, `watch`, `merge`, `land`, `status`, `sweep`;
  aliases: open/raise → create, monitor/ci → watch, ship → land). No verb → `status`
  if a PR exists for the current branch, else `create`.
- PR: an optional number or URL; default the current branch's PR.
- REPO: `--repo owner/name`; default the current repo.
- WAIT TOOL: `pr-wait.sh` lives in `skills/landing-prs/` next to this command's
  plugin root (`${PLUGIN_ROOT}/skills/landing-prs/pr-wait.sh`); run it with
  `bash`, in the background for long waits, and read its `SUMMARY` line.

## create
1. If on `main`/`master`/`develop`: `git checkout -b fix/<slug>` (or `feat/`) first.
2. Commit the pending work (one focused commit; attribution trailer per the
   session's rules), `git push -u origin <branch>`.
3. `gh pr create --base <integration branch> --title … --body …` with the
   Why / Root cause / What changed / Verification shape. `--draft` when the repo is
   Critical tier or the change touches auth, payments, migrations, infra, secrets.
4. Continue with **watch**.

## watch
1. `pr-wait.sh <PR>` — wait for it (it polls; do not poll around it).
2. Triage the digest: every failed check and every `[OPEN]` review thread gets a
   root-cause fix with a test, or a reasoned reply. Push, then re-run step 1.
3. Stop when `checks_failed=0` and `unresolved_threads=0`. Report the final
   digest in a short table. Do **not** merge under this verb.

## merge
1. Run **watch** first (a green digest is the precondition).
2. Refuse on a draft PR, on a Critical-tier repo without the user's explicit go,
   or with `--admin`. Confirm the base branch matches the repo's flow.
3. Read `merge_state` from the pr-wait SUMMARY (`CLEAN`, `BEHIND`, `BLOCKED`,
   `UNKNOWN`, …). If it is `BEHIND` (base moved since the checks ran, and the
   repo requires an up-to-date branch), run `gh pr update-branch <PR>`, then go
   back to step 1 — the checks must pass on the head that will actually merge.
   `BLOCKED` means a rule you cannot satisfy from here (a required review, a
   required check that never ran): report it, never `--admin` past it.
   `UNKNOWN` is not a green light: report it and do not merge.
4. `gh pr merge <PR> --squash --delete-branch` (`--rebase` where the repo prefers
   it). If the repo's `AGENTS.md` names a post-merge deploy step, do it and verify.
5. Report: merged SHA, what deployed, what to watch next.

## land
**create** then **merge**, one flow, no pause between unless something fails.

## status
`pr-wait.sh <PR> --no-wait`; answer: merged or not, checks state, unresolved
threads (quote them), anything in the comments not yet actioned.

## sweep
`gh pr list --state open --json number,title,headRefName,isDraft` for the repo
(or `--repo` for each repo the user names); run **status** on each, then
**watch** the ones with findings and **merge** the ones the user said to merge.
Summarise as one table: PR, state, failures, open threads, action taken.

## Grok Build execution

Use this skill in xAI Grok Build (`grok`). Resolve bundled helper paths relative to this `SKILL.md` file. Read repository `AGENTS.md` instructions first. Use connected Notion/MCP tools when available; do not invent tool names.
