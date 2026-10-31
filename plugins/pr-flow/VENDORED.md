# Vendored copy: pr-flow plugin

Cursor team marketplaces resolve plugin sources as directories inside this catalogue repository, so Cursor installs this directory. Claude, Codex and Copilot pin `plugins/pr-flow` in `Wicked-Sick-Ltd/ai-grok-repo` at the commit below. That commit is already on the upstream default branch, so a squash merge of this catalogue pull request does not drop the pin.

- Canonical upstream: https://github.com/Wicked-Sick-Ltd/ai-grok-repo
- Upstream path: `plugins/pr-flow`
- Version: 1.0.0
- Upstream commit: `2b70a9bf8fe3e98c69451492f7516a549ae798f3` (2026-10-30, `Reduce pr-wait GitHub API usage` #13)
- Upstream contents copied here: `.claude-plugin/plugin.json`, `skills/landing-prs/SKILL.md`, `skills/landing-prs/pr-wait.sh`, `skills/pr/SKILL.md`

Catalogue files added on top of that commit: `.cursor-plugin/plugin.json`, `.codex-plugin/plugin.json`, `plugin.json`, `README.md`, `CHANGELOG.md`, and this file.

One line in this directory's `skills/landing-prs/SKILL.md` is not in the upstream commit. It names review comments from Claude, Bugbot, Copilot, CodeQL and Semgrep: every finding is either fixed or answered, and every thread is resolved before the PR counts as done. Cursor loads that line with this tree. The remote pins load the upstream skill, which already requires every reviewer-bot finding to be answered before the PR is done.

`skills/landing-prs/pr-wait.sh` stays executable (`100755`).
