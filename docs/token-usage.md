# Token usage

Catalog version **0.9.0**. The release tag [v0.9.0](https://github.com/Wicked-Sick-Ltd/token-usage/releases/tag/v0.9.0) is `fe998547b0dfa9472e2a80cb9beee9bae3018575` (2026-10-18). Every Claude, Codex, Copilot and Gemini pin in this repository, and the vendored Cursor copy, point at the later commit `39cbb737084bf4f8aaa0c17b8cd1c560f6a0a47c` (2026-10-21, token-usage #27). Manifests at that commit still say 0.9.0. #27 adds the Antigravity plugin bundle (`plugin.json`, `mcp_config.json`, `hooks.json`) and the multi-runtime report skill on top of the tagged release.

Upstream `main` was `7638fb1b07751f1bfd2d4d6cc535aad71280f905` on 2026-11-13 (token-usage #34). That commit is **not** vendored and **not** pinned here. It adds the `cursor-cloud` runtime described below, plus an opt-in activity-stream bridge that this catalogue does not document and does not ship. Do not treat an install from this marketplace as that `main` tree.

## What this pin can read

| Runtime | Recordings this copy reads | Limit |
| --- | --- | --- |
| Claude Code / Cowork | Claude transcripts and the Stop / SubagentStop ledger | Costs are API list-price estimates, not a subscription bill. |
| Codex | Codex session files | Hook trust is per machine. Codex 0.160.0 could not expand `${PLUGIN_ROOT}` in the 0.7.0 MCP args; 0.8.0+ launches `scripts/mcp_server.py` with `cwd: "."`. |
| Cursor desktop / CLI | Hook ledger under `~/.cache/token-usage/cursor/`, then read-only Desktop `state.vscdb` | `cursor-hook` always prints `{}` and exits 0. It does not emit a budget nudge. |
| Cursor Cloud Agent export | A `.json` file you pass on the command line or as the MCP `transcript` | No network call. Token fields are used only when the file contains `usage` or `tokenUsage`. Otherwise the measurement is `activity_only`. |
| Antigravity / Gemini CLI | `transcript.jsonl` under `~/.gemini/antigravity*/brain/…` and legacy `~/.gemini/tmp/*/chats/` | `--runtime gemini`. Unknown model prices stay unknown. |
| Copilot CLI | Local capture and recovered shutdown totals | Per-call capture needs `--experimental`. No paid-account or IDE billing claim. |

`auto` never mixes two runtimes in one call. This copy's runtime names are `claude`, `cursor`, `codex`, `gemini`, `copilot`, and `auto`. There is no `cursor-cloud` name in `plugins/token-usage/scripts/token_usage.py`.

Python 3.9+ is required. macOS and Linux need `python3` on `PATH`. The Cursor MCP entry sets `TOKEN_USAGE_RUNTIME=cursor` and `PYTHONUTF8=1`.

## Environment variables in this copy

| Variable | Role |
| --- | --- |
| `TOKEN_USAGE_RUNTIME` | Default runtime for the CLI and MCP process (`claude` if unset). The Cursor plugin sets `cursor`. |
| `TOKEN_USAGE_CURSOR_DIR` | Cursor user directory. Unset: `~/Library/Application Support/Cursor/User` on macOS, `~/.config/Cursor/User` on Linux, `%APPDATA%\Cursor\User` on Windows. |
| `TOKEN_USAGE_LEDGER_DIR` | Shared ledger root. Unset: `~/.cache/token-usage`. Cursor hook files live in `$TOKEN_USAGE_LEDGER_DIR/cursor/` (default `~/.cache/token-usage/cursor/`). Pointing this variable at the `cursor` directory itself makes discovery look one level too deep. The `cursor` directory is created owner-only (`0700`) when the filesystem allows it. |
| `TOKEN_USAGE_TRANSCRIPT` | Claude, Codex, Gemini, and Copilot only. Claude exits if the path is missing. Cursor ignores it: pass the export path as the CLI argument or the MCP `transcript`. |
| `TOKEN_USAGE_PROJECTS_DIR` | Claude projects directory used by history and insights. |
| `TOKEN_USAGE_GEMINI_HOME` | Antigravity / Gemini home. Unset: `~/.gemini`. |
| `TOKEN_USAGE_CODEX_HOME` or `CODEX_HOME` | Codex home. |
| `TOKEN_USAGE_COPILOT_HOME` or `COPILOT_HOME` | Copilot CLI home. |
| `TOKEN_USAGE_BUDGET_USD` | Positive number of USD. Claude, Codex and Antigravity Stop hooks can emit one `systemMessage` per crossed multiple. The Cursor hook ignores it and prints `{}`. |
| `CURSOR_PLUGIN_ROOT` | Set by Cursor for hook and MCP paths. Not a token-usage setting. |

The hook ledger stores the conversation id, timestamps, workspace roots, raw token fields, and the first 120 characters of each prompt. Transcripts themselves stay on disk where the host wrote them. This copy does not call Cursor, Codex, Gemini, Copilot or Claude APIs.

## Cursor Cloud Agents

Two different mechanisms exist. Only the first is in the catalogue pin.

### Explicit export (installed today)

Cursor Cloud Agents do not inherit a developer's local plugin, `~/.cursor` hooks, or `~/.cursor/mcp.json`. A cloud VM runs repository hooks from `.cursor/hooks.json`. This marketplace does not ship that file, so a cloud run does not load token-usage unless the VM image or the repository under analysis adds it.

From a checkout of this catalogue, the script is `plugins/token-usage/scripts/token_usage.py`. Inside a token-usage checkout the same file is `scripts/token_usage.py`.

```bash
python3 plugins/token-usage/scripts/token_usage.py report --runtime cursor /path/to/cloud-export.json
python3 plugins/token-usage/scripts/token_usage.py json --runtime cursor /path/to/cloud-export.json
```

The same path is the MCP `transcript` argument with `runtime: "cursor"`. The selector must be an existing `.json` object. A `.jsonl` path is rejected. Composer ids are accepted as MCP `session_id`, not as a CLI positional argument.

Limits, from `plugins/token-usage/scripts/token_usage.py`:

- The adapter reads `messages[]` with `role`, text, optional `model`, and optional `usage` / `tokenUsage`.
- A file with token fields on at least one turn is `partial` (the caller treats `saw_tokens` as partial, not exact).
- A file with no token fields is `activity_only`: a count of turns, not a token bill. Nothing is inferred from message length.
- The developer's laptop ledger does not contain the cloud run. If the VM has the plugin, or a `.cursor/hooks.json` that runs `plugins/token-usage/scripts/token_usage.py cursor-hook`, the ledger on that VM is the higher-confidence source. Read it there. To read a copy elsewhere, copy the `cursor` directory into the ledger root (`~/.cache/token-usage/cursor/`, or `$TOKEN_USAGE_LEDGER_DIR/cursor/`) and pass `--runtime cursor`. Do not set `TOKEN_USAGE_LEDGER_DIR` to the `cursor` directory itself.

Ask the agent, once the MCP server is on that VM, to call `session_cost` with `runtime: "cursor"` and to include `measurement` and `warnings`.

### `cursor-cloud` runtime (upstream `main` only)

Cloud Agent runs (`bc-…` ids) leave nothing in the local Cursor database, and their transcripts often carry no token counts, so the `cursor` runtime cannot price them. Upstream `main` (`7638fb1b07751f1bfd2d4d6cc535aad71280f905`, token-usage #34, unreleased) adds an opt-in runtime that syncs Cursor's Admin API.

That code is **not** in `plugins/token-usage/` and **not** in the SHA pins. Installing `token-usage@wickedsick` from this marketplace does not provide `cursor-cloud-sync` or `--runtime cursor-cloud`. The notes below are the upstream contract, so a later pin bump has a written target. They were taken from the upstream README and changelog on 2026-11-14.

These commands are for a checkout of upstream token-usage, where the script is `scripts/token_usage.py`. They are not paths in this catalogue.

```bash
export CURSOR_ADMIN_API_KEY=…            # Team Admin API key, read scope
export CURSOR_API_KEY=…                  # optional user key: agent name and repository
python3 scripts/token_usage.py cursor-cloud-sync --since 7d
python3 scripts/token_usage.py top_consumers --runtime cursor-cloud --since 7d
python3 scripts/token_usage.py report --runtime cursor-cloud bc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
python3 scripts/token_usage.py history --runtime cursor-cloud --by model
```

Upstream limits:

- One session per agent run, one activity segment per conversation per local day. The project is the agent's repository when `CURSOR_API_KEY` is set, otherwise `cursor-cloud`.
- Cost is Cursor's `chargedCents` (model cost plus any Cursor Token Rate), not the bundled pricing table. Usage paid from a credit grant shows `0`.
- `measurement` is `exact` when every call carried token counts and `partial` when some were request-billed without tokens.
- Ledgers live under `~/.cache/token-usage/cursor-cloud/` (`TOKEN_USAGE_CURSOR_CLOUD_DIR`). They store timestamp, agent / conversation / automation ids, model, billing kind, token counts and `chargedCents`, plus an optional header with the agent's name and repository. They do not store user emails, prompts or the API key.
- With the admin key set, scans refresh at most every 15 minutes (`TOKEN_USAGE_CURSOR_CLOUD_SYNC_INTERVAL`). `TOKEN_USAGE_CURSOR_CLOUD_AUTOSYNC=0` reads cached ledgers only. Without a key the runtime is read-only and makes no network call.
- Cursor aggregates usage events hourly, so the latest calls can take up to an hour to appear. Each sync re-reads a three-hour overlap and replaces it. An empty API answer does not erase a ledger. Concurrent syncs use a lock file.
- `auto` never selects `cursor-cloud`.

Do not commit `CURSOR_ADMIN_API_KEY` or `CURSOR_API_KEY`.

## Catalog verification (historical)

These checks were recorded against earlier candidates. They are not a re-test of `39cbb737` on 2026-11-14.

| Host | Evidence | Limit |
| --- | --- | --- |
| Claude Code | Native manifest validator and MCP connection; existing parser/hook suite | Directory portal submission remains a separate owner action. |
| Codex 0.160.0 | Isolated plugin install, app-server listing and five-tool discovery for the 0.8.0 candidate | Hook trust remains per machine. |
| Cursor CLI 2026.10.01-e373342 | Manual MCP registration, five tools; synthetic parser/hook tests | Desktop plugin UI was not exercised in that pass. |
| Antigravity / Gemini CLI 0.62.0 | Antigravity bundle and `transcript.jsonl` parser, plus legacy Gemini fixtures, at the 0.9.0 work | Legacy Gemini CLI remains the fallback install. |
| Copilot CLI 1.0.91 | Plugin install and native offline tests | Requires `--experimental` for per-call capture. A local-directory marketplace did not load the plugin afterward; the GitHub marketplace route did. |

Privacy notes for the tagged release: [Gemini/Copilot](https://github.com/Wicked-Sick-Ltd/token-usage/blob/fe998547b0dfa9472e2a80cb9beee9bae3018575/docs/gemini-copilot.md) and [privacy](https://github.com/Wicked-Sick-Ltd/token-usage/blob/fe998547b0dfa9472e2a80cb9beee9bae3018575/README.md#privacy-and-data-handling). The pin's own README is the tree at `39cbb737`. Current upstream privacy text, including `cursor-cloud`, is on `main` and is not what this pin installs.
