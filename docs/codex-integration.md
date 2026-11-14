# Codex integration and troubleshooting

`ai-marketplace` is the entry point; `ai-codex-repo` owns the first-party
Codex packages, setup and private configuration. The public index contains **ten**
native packages. Organisation access is required for the first-party sources.

## Current Codex entries

From `.agents/plugins/marketplace.json`. None of these entries set a `version` field. The SHA is the pin.

| Plugin | Source | SHA |
| --- | --- | --- |
| estate-maintenance | `ai-codex-repo` `plugins/estate-maintenance` | `06f5c0a19808e91ccc53bba9111346fdbb86ee23` |
| onboarding | `ai-codex-repo` `plugins/onboarding` | `06f5c0a19808e91ccc53bba9111346fdbb86ee23` |
| product-lifecycle | `ai-codex-repo` `plugins/product-lifecycle` | `06f5c0a19808e91ccc53bba9111346fdbb86ee23` |
| session-lifecycle | `ai-codex-repo` `plugins/session-lifecycle` | `06f5c0a19808e91ccc53bba9111346fdbb86ee23` |
| wizzo-fleet-presence | `ai-codex-repo` `plugins/wizzo-fleet-presence` | `06f5c0a19808e91ccc53bba9111346fdbb86ee23` |
| amiga-decoding | this repo `./plugins/amiga-decoding` | none (vendored directory) |
| pr-flow | `ai-grok-repo` `plugins/pr-flow` | `62272ec3ec8eba9059fd43ce9a9d1f913e317fbb` |
| token-usage | `Wicked-Sick-Ltd/token-usage` root | `39cbb737084bf4f8aaa0c17b8cd1c560f6a0a47c` |
| ponytail | `DietrichGebert/ponytail` root | `e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156` |
| publicuniverse | `Wicked-Sick-Ltd/public-universe` root | `bb5919e47e8c8e1eb66c2fc5dcdba9bbc51b2f56` |

`ai-codex-repo` `main` was `e4e911ab30ecbb179c318c60681210d9f25de2d5` on 2026-11-05 (ready-for-review rule in that repo's own landing-prs). This index still pins five first-party packages at `06f5c0a`. **amiga-decoding** is not one of them: Codex installs `./plugins/amiga-decoding` from this public repository, the same directory Cursor installs. That entry has no SHA and no `version` field, matching the other Codex entries. `pr-flow` here is the ai-grok-repo 1.0.0 tree, not the 1.1.0 Cursor directory and not current ai-grok-repo `main`. `publicuniverse` 0.4.1 still configures `https://api.sol.wickedsick.com/mcp`. `token-usage` does not include the unreleased `cursor-cloud` runtime. This page does not move those pins.

## Packaging correction

The old fleet listing pointed at the root of `ai-codex-repo`. That directory
contained a separate configuration installer, not a native plugin manifest.
Codex could accept the listing by synthesizing a minimal manifest, so an
apparently successful install did not establish lifecycle-hook installation.

The index now selects `plugins/<name>` using `git-subdir`, with real
`.codex-plugin/plugin.json` resources. token-usage and Ponytail select their
upstream root packages. `pr-flow` is pinned to `plugins/pr-flow` in
`Wicked-Sick-Ltd/ai-grok-repo` (the canonical package). The Cursor
catalogue copy under `plugins/pr-flow/` here also ships
`.codex-plugin/plugin.json` and the portable root `plugin.json`.
Every remote source is pinned by SHA; the validator
rejects missing or malformed pins and escaping subdirectory paths.

The earlier claim that Codex had no `sha` or `ref` field was incorrect for the
tested runtime. See the [official plugin documentation](https://developers.openai.com/plugins/build/plugins).

## If adding or installing fails

Check `codex --version`, then retry the exact command in the
[README](../README.md). Distinguish marketplace registration from individual
plugin installation: registration reads this public index; first-party installs
also need authenticated Git access to `Wicked-Sick-Ltd/ai-codex-repo`, except
**amiga-decoding**, whose source is `./plugins/amiga-decoding` in this checkout.
A `--sparse .agents/plugins` marketplace add does not include that directory.

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

2026-10-05 update: Codex 0.160.0 installed token-usage 0.7.0 but its MCP launcher
failed because a legacy argument placeholder was passed literally. The 0.8.0
candidate fixes startup and listing metadata. Its isolated native install and
five-tool discovery were verified again; see [the candidate record](token-usage.md).
The older successful MCP observation below does not establish compatibility of
0.7.0 with 0.160.0. The catalogue pin is now `39cbb737` (manifest 0.9.0), which
was not the build under that October check.

Tested with Codex CLI 0.159.3 on Windows, against the eight-package index of that
date (the index now has ten entries; `pr-flow` and `publicuniverse` were added
later):

- Marketplace registration from GitHub succeeded in an isolated `CODEX_HOME`.
- All eight entries then listed installed from their pinned remote sources with real native
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
