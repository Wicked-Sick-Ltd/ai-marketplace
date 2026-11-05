# Vendored copy: pr-flow plugin

Cursor team marketplaces resolve plugin sources as directories inside this catalogue repository, so Cursor installs this directory. Claude, Codex and Copilot pin `plugins/pr-flow` in `Wicked-Sick-Ltd/ai-grok-repo` at the commit below. That commit is already on the upstream default branch, so a squash merge of this catalogue pull request does not drop the pin.

- Canonical upstream: https://github.com/Wicked-Sick-Ltd/ai-grok-repo
- Upstream path: `plugins/pr-flow`
- Catalogue version: 1.1.0. Every manifest in this directory is 1.1.0, including `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.cursor-plugin/plugin.json`, and `plugin.json`. Those files describe this directory. A host that installs this directory gets 1.1.0. Cursor's marketplace entry does that.
- Upstream commit: `62272ec3ec8eba9059fd43ce9a9d1f913e317fbb` (2026-10-31, `Count every reviewer bot before a PR is done` #14)
- Updated in this directory after that commit: `skills/landing-prs/SKILL.md`, `skills/pr/SKILL.md`, and the manifest versions above. `.claude-plugin/plugin.json` was copied from the upstream commit and then bumped with the rest of this directory.
- Unchanged from that commit: `skills/landing-prs/pr-wait.sh` (stays executable, `100755`)

Catalogue files added on top of that commit: `.cursor-plugin/plugin.json`, `.codex-plugin/plugin.json`, `plugin.json`, `README.md`, `CHANGELOG.md`, and this file.

Hosted Claude, Codex, and Copilot marketplace entries do not install this directory, and they do not read `.claude-plugin/plugin.json` from it. They install `plugins/pr-flow` from `ai-grok-repo` at `62272ec3ec8eba9059fd43ce9a9d1f913e317fbb`. That commit's manifests are still 1.0.0, and its skills do not contain the 5 Nov 2026 rule. Those pins stay there until the same rule is on the upstream default branch. A pin to this catalogue pull request would disappear on squash merge.

`skills/landing-prs/SKILL.md` keeps that commit's done criteria: review comments from Claude, Bugbot, Copilot, CodeQL and Semgrep all count, every finding is fixed or answered, and every thread is resolved, before the PR counts as done. CI on the head commit is green. Catalogue version 1.1.0 adds Craig's standing rule from 5 Nov 2026 in `skills/landing-prs/SKILL.md` and `skills/pr/SKILL.md`: a finished PR is opened ready for review (no `--draft`), or an existing draft is marked ready with `gh pr ready <PR> --repo <OWNER/REPO>`, Critical-tier PRs included. The `pr` command passes the selected PR and repository so it cannot ready a different current-branch PR. A draft is only for work still in progress. A finished PR left as draft is a red flag.
