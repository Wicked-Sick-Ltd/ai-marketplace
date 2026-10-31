# Vendored copy: pr-flow plugin

Cursor team marketplaces resolve plugin sources as directories inside this catalogue repository, so Cursor installs this directory. Claude, Codex and Copilot pin `plugins/pr-flow` in `Wicked-Sick-Ltd/ai-grok-repo` at the commit below. That commit is already on the upstream default branch, so a squash merge of this catalogue pull request does not drop the pin.

- Canonical upstream: https://github.com/Wicked-Sick-Ltd/ai-grok-repo
- Upstream path: `plugins/pr-flow`
- Version: 1.0.0
- Upstream commit: `62272ec3ec8eba9059fd43ce9a9d1f913e317fbb` (2026-10-31, `Count every reviewer bot before a PR is done` #14)
- Upstream contents copied here: `.claude-plugin/plugin.json`, `skills/landing-prs/SKILL.md`, `skills/landing-prs/pr-wait.sh`, `skills/pr/SKILL.md`

Catalogue files added on top of that commit: `.cursor-plugin/plugin.json`, `.codex-plugin/plugin.json`, `plugin.json`, `README.md`, `CHANGELOG.md`, and this file.

`skills/landing-prs/SKILL.md` matches that commit, including the triage line that review comments from Claude, Bugbot, Copilot, CodeQL and Semgrep all count: every finding is fixed or answered, and every thread is resolved, before the PR counts as done. Claude, Codex and Copilot install that same commit.

`skills/landing-prs/pr-wait.sh` stays executable (`100755`).
