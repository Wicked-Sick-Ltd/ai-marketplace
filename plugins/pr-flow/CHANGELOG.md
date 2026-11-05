# Changelog

## 1.1.0 (2026-11-05)

### Changed

- `landing-prs` and `pr`: Craig's standing rule (5 Nov 2026). When a cloud agent finishes its work, open the PR ready for review (no `--draft`) or run `gh pr ready <pr> --repo <owner/name>` on an existing draft, so reviewers and CI start straight away. A draft is only allowed while work is still in progress, Critical-tier PRs included. A finished PR left as draft is a red flag. The `pr` command always passes the selected PR and repository, so a bare `gh pr ready` cannot mark a different current-branch PR ready.
- Done criteria are unchanged: Claude, Bugbot, Copilot, CodeQL and Semgrep have run, every finding is fixed or answered, every thread is resolved, and CI is green.

## 1.0.0 (2026-10-31)

### Added

- Catalogue copy of `pr-flow` from `Wicked-Sick-Ltd/ai-grok-repo` `plugins/pr-flow` at `62272ec3ec8eba9059fd43ce9a9d1f913e317fbb`, so Cursor, Claude, Codex and Copilot can install `landing-prs` from this marketplace.
- Cursor, Claude, Codex and portable plugin manifests for that package.

### Changed

- `landing-prs` matches upstream #14: review comments from Claude, Bugbot, Copilot, CodeQL and Semgrep all count, and every finding is fixed or answered and every thread resolved before the PR counts as done. Claude, Codex and Copilot pins are that commit.
