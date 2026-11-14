# token-usage (catalogue copy)

Cursor team marketplaces install this directory. Claude, Codex, Copilot and the Gemini install command install the same commit from GitHub: `39cbb737084bf4f8aaa0c17b8cd1c560f6a0a47c`. Manifest version **0.9.0**. The v0.9.0 tag is the earlier commit `fe998547b0dfa9472e2a80cb9beee9bae3018575`. See [VENDORED.md](VENDORED.md).

Upstream: https://github.com/Wicked-Sick-Ltd/token-usage

This copy attributes recorded token usage for Claude Code, Cowork, Codex, Cursor, Google Antigravity, Gemini CLI and Copilot CLI. Costs are API list-price estimates, not a subscription bill. Python 3.9+ and `python3` on `PATH`.

## Cursor Cloud Agents

This copy does **not** include the unreleased `cursor-cloud` runtime on upstream `main` (`7638fb1b07751f1bfd2d4d6cc535aad71280f905`). It cannot call the Cursor Admin API.

What it can do:

- Report a Cloud Agent export you already have:

  ```bash
  python3 scripts/token_usage.py report --runtime cursor /path/to/cloud-export.json
  ```

  The file must be a `.json` object. Token counts are taken from `usage` or `tokenUsage` when those fields exist. A file with none is `activity_only` (turns, not a bill). Message length is not turned into tokens.

- If the cloud VM has this plugin, or the repository under analysis has a `.cursor/hooks.json` that runs `scripts/token_usage.py cursor-hook`, the hook ledger on that VM (`~/.cache/token-usage/cursor/`, or `TOKEN_USAGE_LEDGER_DIR`) is the higher-confidence source. A developer's laptop ledger does not contain the cloud run. Cloud Agents do not inherit `~/.cursor` plugins or `~/.cursor/mcp.json`.

The Cursor hook always prints `{}` and exits 0. `TOKEN_USAGE_BUDGET_USD` does not nudge Cursor.

Full setup, environment variables and the upstream-only `cursor-cloud` contract: [`docs/token-usage.md`](../../docs/token-usage.md).
