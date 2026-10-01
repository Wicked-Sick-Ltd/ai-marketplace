# Codex integration and troubleshooting

`ai-marketplace` is the entry point; `ai-codex-repo` owns the first-party
Codex packages, setup and private configuration. The public index contains eight
native packages. Organisation access is required for the first-party sources.

## Packaging correction

The old fleet listing pointed at the root of `ai-codex-repo`. That directory
contained a separate configuration installer, not a native plugin manifest.
Codex could accept the listing by synthesizing a minimal manifest, so an
apparently successful install did not establish lifecycle-hook installation.

The index now selects `plugins/<name>` using `git-subdir`, with real
`.codex-plugin/plugin.json` resources. token-usage and Ponytail select their
upstream root packages. Every remote source is pinned by SHA; the validator
rejects missing or malformed pins and escaping subdirectory paths.

The earlier claim that Codex had no `sha` or `ref` field was incorrect for the
tested runtime. See the [official plugin documentation](https://developers.openai.com/plugins/build/plugins).

## If adding or installing fails

Check `codex --version`, then retry the exact command in the
[README](../README.md). Distinguish marketplace registration from individual
plugin installation: registration reads this public index; first-party installs
also need authenticated Git access to `Wicked-Sick-Ltd/ai-codex-repo`.

On Windows, `Filename too long` or `cannot write keep file` during a plugin
clone can come from Git's staging path. Reproduced with a deeply nested temporary
`CODEX_HOME`; the identical install succeeded with a shorter home, and also with
`core.longpaths=true` supplied to the child Git process. A setting in the current
repository's `.git/config` does not apply to Codex's fresh plugin clones.
If this is the error, the user-level Git remedy is:

```powershell
git config --global core.longpaths true
```

Then retry the failed operation. This changes Git for that user; the diagnostic
tests used process-scoped configuration and did not change the real user profile.
The initial marketplace-add command itself succeeded in testing; these findings
do not establish which error occurred in a separate session.

## Validation evidence (2026-10-01)

Tested with Codex CLI 0.159.3 on Windows:

- Marketplace registration from GitHub succeeded in an isolated `CODEX_HOME`.
- All eight entries installed from their pinned remote sources with real native
  manifests, including private first-party sources and public upstream plugins.
- Codex app-server discovered all 34 expected public skills and fleet, handoff
  and token-usage hooks. The installed token-usage MCP server also initialized
  successfully and exposed its five tools.
- The private vendor catalog was separately checked for complete coverage of
  its Claude reference. Vendor CI validates Windows, macOS and Linux behavior.
- Catalog validation and regression tests passed.

These checks did not launch a live agent thread, grant hook trust or contact
production MCP/mesh services. Review hooks through `/hooks` and complete service
sign-in on each target machine. The existing config-based presence block must
be removed before enabling the native fleet plugin to avoid duplicate events.
