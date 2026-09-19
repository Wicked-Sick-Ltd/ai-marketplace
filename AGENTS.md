# Agent instructions

This repository is an **index**. It lists plugins; it does not contain plugin code.

- Do not vendor plugin sources here.
- Claude entries are pinned to a full 40-character commit SHA (`git-subdir` + `sha`). Codex's Agent Plugins schema has no ref/sha field, so Codex entries name the repo URL and Codex resolves its default branch; the SHA of record for a Codex pack lives in the audit doc and that repo's merge commit, not in the index.
- Cursor's `.cursor-plugin/marketplace.json` uses **in-repo paths** only (`source` is a directory in this git tree, optionally under `metadata.pluginRoot`). Do not copy Claude `github`/`sha` source objects there. Cursor Team Marketplace should import the repo that contains the plugin directories (`claude-repo`), not vendor those plugins here.
- List a plugin only on the catalogs where it has a real runtime.
- `token-usage` stays on the Claude index until other hosts have a parser or an honest "Claude transcripts only" listing.
- After catalog edits, run `python3 scripts/validate.py`.

Product-repo agent rules (Forge, Yaegi, Traefik) live in those repos, not here.

## Cursor Cloud: Dependabot API access

The built-in Cloud Agent GitHub App token cannot call the Dependabot alerts API. For triage, inject a fine-grained PAT as `GH_TOKEN` with **Dependabot alerts: Read**, then run `python3 scripts/dependabot_alerts.py --check`. Details: [`docs/github-security-api-access.md`](docs/github-security-api-access.md).
