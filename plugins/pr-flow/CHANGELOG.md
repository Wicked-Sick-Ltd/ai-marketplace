# Changelog

## 1.0.0 (2026-10-31)

### Added

- Catalogue copy of `pr-flow` from `Wicked-Sick-Ltd/ai-grok-repo` `plugins/pr-flow` at `62272ec3ec8eba9059fd43ce9a9d1f913e317fbb`, so Cursor, Claude, Codex and Copilot can install `landing-prs` from this marketplace.
- Cursor, Claude, Codex and portable plugin manifests for that package.

### Changed

- `landing-prs` matches upstream #14: review comments from Claude, Bugbot, Copilot, CodeQL and Semgrep all count, and every finding is fixed or answered and every thread resolved before the PR counts as done. Claude, Codex and Copilot pins are that commit.
