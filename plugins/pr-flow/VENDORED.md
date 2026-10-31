# Vendored copy: pr-flow plugin

Cursor team marketplaces resolve plugin sources as directories inside this catalogue repository. Claude, Codex and Copilot install the same directory from a commit pin of this repository, so every host loads this tree.

- Canonical upstream: https://github.com/Wicked-Sick-Ltd/ai-grok-repo
- Upstream path: `plugins/pr-flow`
- Version: 1.0.0
- Upstream commit: `2b70a9bf8fe3e98c69451492f7516a549ae798f3` (2026-10-30, `Reduce pr-wait GitHub API usage` #13)
- Upstream contents copied here: `.claude-plugin/plugin.json`, `skills/landing-prs/SKILL.md`, `skills/landing-prs/pr-wait.sh`, `skills/pr/SKILL.md`

Catalogue files added on top of that commit: `.cursor-plugin/plugin.json`, `.codex-plugin/plugin.json`, `plugin.json`, `README.md`, `CHANGELOG.md`, and this file.

One line in `skills/landing-prs/SKILL.md` is not in the upstream commit. It names review comments from Claude, Bugbot, Copilot, CodeQL and Semgrep: every finding is either fixed or answered, and every thread is resolved before the PR counts as done.

`skills/landing-prs/pr-wait.sh` stays executable (`100755`).
