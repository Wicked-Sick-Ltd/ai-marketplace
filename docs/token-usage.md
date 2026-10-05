# Token usage: 0.8.0 candidate

The companion [token-usage PR](https://github.com/Wicked-Sick-Ltd/token-usage/pull/20)
repairs Codex installation and adds Gemini CLI/Copilot CLI support while preserving
Claude Code and Cursor. This catalog update is a release candidate, not an approval
to publish. The plugin PR has merged at `ae989e2cde864447f8c63c1423c0d4ba3b9839df`; approve its
0.8.0 release before merging these catalog pins. If the reviewed tree changes, update every pin together.

## What failed in Codex

Codex 0.160.0 could install the 0.7.0 package, but its legacy MCP configuration did
not expand `${PLUGIN_ROOT}` in arguments. Python received a literal path and the
MCP handshake failed. The fix uses `cwd: "."` with `scripts/mcp_server.py`.

The native listing comes from `.codex-plugin/plugin.json`'s `interface` metadata,
not this catalog's description. The candidate fills its description, developer and
website there. An isolated install and app-server check verified the listing and
all five tools. Advancing the catalog SHA brings both fixes into the installed package.

## Verified surfaces

| Host | Evidence | Limit |
|---|---|---|
| Claude Code | Native manifest validator and MCP connection; existing parser/hook suite | Directory portal submission remains a separate owner action. |
| Codex 0.160.0 | Actual isolated plugin install, app-server listing and five-tool discovery | Hook trust remains per machine. |
| Cursor CLI 2026.10.01-e373342 | Manual MCP registration ready, five tools; synthetic parser/hook tests | Desktop plugin/marketplace UI not exercised. This repository cannot list external plugin paths in its Cursor index. |
| Gemini CLI 0.62.0 | Extension validation, pinned Git install, report skill and Connected MCP; JSON/JSONL fixtures | No model-driven turn tested. Local install/link operations emitted a Windows Node/libuv shutdown assertion; the pinned Git install completed cleanly. |
| Copilot CLI 1.0.91 | Plugin install, skill/server discovery, native offline tests with synthetic OpenAI/Anthropic responses and resumed sessions | Requires `--experimental` for per-call capture; no paid-account or IDE support claim. |

Token counts use recorded fields. Missing counters yield partial/activity-only
reports, and unknown model prices remain unknown. Costs are API estimates, not
subscription charges. The Copilot collector stores labels and counters locally,
without prompt or tool text. See upstream
[Gemini/Copilot notes](https://github.com/Wicked-Sick-Ltd/token-usage/blob/ae989e2cde864447f8c63c1423c0d4ba3b9839df/docs/gemini-copilot.md)
and [privacy disclosures](https://github.com/Wicked-Sick-Ltd/token-usage/blob/ae989e2cde864447f8c63c1423c0d4ba3b9839df/README.md#privacy-and-data-handling).

Claude, Codex and Copilot catalogs pin the same commit. Gemini's install command
uses that commit as `--ref`. Cursor users import the token-usage repository itself
or register the local MCP server; no plugin source is vendored here.

## Catalog verification

The branch catalog installed 0.8.0 in isolated Claude and Copilot profiles from
GitHub; both discovered the MCP server, and Claude reported Connected. Codex
installed the same remote SHA from the local candidate catalog. Claude's GitHub
source selected SSH on this machine, which has no GitHub host key; the verification
used a process-only Git rewrite to HTTPS, with no SSH trust or global Git changes.
Gemini installed the exact Git SHA, listed version 0.8.0 and its report skill, and
reported the MCP server Connected.

Copilot 1.0.91 displayed a successful install from a local directory marketplace
containing remote URL entries but did not load the plugin afterward. Registering
the actual GitHub branch marketplace loaded it correctly. Validate distribution
through the GitHub route documented in the README, not that local-directory shortcut.

Upstream PR #20 completed 11 checks with zero failures, including Python 3.9/3.12,
native Copilot on Windows/Linux, Claude validation and security scans. Bugbot was
paused by the team's spend limit and did not provide a review; no review threads
were open. The merged tree matches the tested PR head.
