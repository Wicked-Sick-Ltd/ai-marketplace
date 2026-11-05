# Vendored copy: pr-flow plugin

Cursor team marketplaces resolve plugin sources as directories inside this catalogue repository, so Cursor installs this directory. Claude, Codex and Copilot pin `plugins/pr-flow` in `Wicked-Sick-Ltd/ai-grok-repo` at the commit below. That commit is already on the upstream default branch, so a squash merge of this catalogue pull request does not drop the pin.

- Canonical upstream: https://github.com/Wicked-Sick-Ltd/ai-grok-repo
- Upstream path: `plugins/pr-flow`
- Catalogue version: 1.1.0
- Upstream commit: `62272ec3ec8eba9059fd43ce9a9d1f913e317fbb` (2026-10-31, `Count every reviewer bot before a PR is done` #14)
- Upstream contents copied here, then updated in this catalogue: `.claude-plugin/plugin.json`, `skills/landing-prs/SKILL.md`, `skills/pr/SKILL.md`
- Unchanged from that commit: `skills/landing-prs/pr-wait.sh` (stays executable, `100755`)

Catalogue files added on top of that commit: `.cursor-plugin/plugin.json`, `.codex-plugin/plugin.json`, `plugin.json`, `README.md`, `CHANGELOG.md`, and this file.

`skills/landing-prs/SKILL.md` keeps that commit's done criteria: review comments from Claude, Bugbot, Copilot, CodeQL and Semgrep all count, every finding is fixed or answered, and every thread is resolved, before the PR counts as done. CI on the head commit is green. Catalogue version 1.1.0 adds Craig's standing rule from 5 Nov 2026 in `skills/landing-prs/SKILL.md` and `skills/pr/SKILL.md`: a finished PR is opened ready for review (no `--draft`), or an existing draft is marked ready with `gh pr ready`, Critical-tier PRs included. A draft is only for work still in progress. A finished PR left as draft is a red flag.

Cursor installs this directory, so Cursor gets 1.1.0. Claude, Codex and Copilot still install the pinned upstream commit, which does not contain the 5 Nov 2026 rule. Those pins stay on `62272ec3ec8eba9059fd43ce9a9d1f913e317fbb` until the same rule is on the upstream default branch. A pin to this catalogue pull request would disappear on squash merge.
