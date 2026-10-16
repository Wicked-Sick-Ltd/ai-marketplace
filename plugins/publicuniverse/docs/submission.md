# PublicUniverse public distribution

Release candidate: 0.4.1. The package is prepared for Cursor marketplace review, not approved for other public directories. Client evidence is recorded in [validation.md](validation.md).

## Identity and migration

- Package and client namespace: `publicuniverse`; display name: Public Universe.
- Repository: `Wicked-Sick-Ltd/public-universe` (rename of `solar-plugin`; GitHub keeps redirects from the old name for web, API and git URLs).
- Website: `https://publicuniverse.net`, matching the website repository's canonical deployment configuration.
- Audit skill: `publicuniverse-data-audit` replaces `solar-data-audit`. The other six skill names stay the same.
- MCP identifier: `publicuniverse` from 0.4.0 (was `solar-system-db`). Skills refer to the new identifier; tool names are unchanged.
- MCP URL: `https://api.sol.wickedsick.com/mcp` (Streamable HTTP, no auth). Initialized successfully on 2026-10-16 with 33 read-only tools and live `get_stats` / `get_object` calls (see validation.md). Keep this URL until `https://api.publicuniverse.net/mcp` is confirmed in production.
- Public catalog: `Wicked-Sick-Ltd/ai-marketplace`. Its Claude, Codex and Copilot indexes pin the plugin source revision; Gemini has an installation guide. Cursor imports the plugin source repository directly because this index does not vendor plugin directories.

Existing users should disable/remove the old `solar` plugin before enabling `publicuniverse`, using their client's plugin manager. Update explicit `/solar:…` invocations to `/publicuniverse:…` on Claude and any copied audit-skill directory after comparing local edits. Do not install both a full plugin and its standalone MCP profile, or overwrite unrelated client configuration.

## Repository and domain rollout

1. **Done:** repository is `Wicked-Sick-Ltd/public-universe` (public; GitHub redirects `solar-plugin`).
2. **Done:** `plugin.json.repository` and generated profiles point at the public repository.
3. Pin the reviewed package commit in remote catalog listings (`ai-marketplace`) and the Gemini install command when submitting those directories.
4. Optional: cut over MCP to `https://api.publicuniverse.net/mcp` when DNS and the service owner confirm the host; update root `mcp.json` and run `python3 scripts/package.py generate`.
5. Record native Cursor desktop acceptance after marketplace listing; package and live MCP checks passed on 2026-10-16.

The generated ZIP and `.plugin` contain the same allowlisted files; neither includes Git history, credentials, development tests or unrelated local files. The icon is reused from the website's existing favicon.

## Official public directories

The Wicked Sick catalog and vendor-operated directories are separate distribution routes. No official submission has been sent. Requirements were checked on 2026-10-05:

- [OpenAI submission](https://developers.openai.com/plugins/deploy/submission) and [validation requirements](https://developers.openai.com/plugins/deploy/submission-errors): listing metadata and square icons are supplied. Remote MCP submission still needs a healthy production endpoint, domain verification, current tool scan, per-tool annotation justifications, verified developer/business identity and attestations, HTTPS support/privacy/terms URLs, and a demo recording. Confirm the public policy pages and their applicability to MCP requests; do not invent URLs or attestations.
- [Claude directory](https://claude.com/blog/build-plugins-for-claude): submit the final public repository through the directory portal after the same runtime acceptance checks.
- [Cursor publishing](https://prod.cursor.com/docs/reference/plugins): submit the plugin source repository through Cursor's publishing flow; its portable skills/MCP package is supported. Do not add a remote SHA object to the path-only Cursor index in `ai-marketplace`.
- [Gemini extensions](https://geminicli.com/docs/extensions/reference/): distribute the native extension from the final public repository; gallery review is separate from CLI installation.
- [Copilot distribution](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference): use the pinned `.github/plugin/marketplace.json` entry and verify installation in the supported CLI/VS Code versions.

## Reviewer scenarios

These are proposed acceptance cases, not recorded successes. OpenAI remote submissions require five positive and three negative cases; record actual tool calls and outcomes when the server is healthy.

| Type | Prompt | Expected result |
| --- | --- | --- |
| Positive | Explain Mars to a ten-year-old using PublicUniverse. | Object lookup, sourced facts, units and age-appropriate explanation. |
| Positive | What can I see tonight from Romsey in Europe/London time? | Location/time handling, live sky calls, local times and Sun safety. |
| Positive | Make a Year 5 worksheet about planets. | Live catalogue data, worksheet and matching answers. |
| Positive | Check whether Venus's day is longer than its year. | Distinguish sidereal rotation from solar day and cite retrieved values. |
| Positive | Draft the next week's sky roundup for London. | Dated tool-backed claims, appropriate links and uncertainty. |
| Negative | What can I see tonight? (no location) | Ask for location before claiming local visibility. |
| Negative | Retrieve Mars while the MCP server is disconnected. | Explain unavailable live data; no fabricated lookup. |
| Negative | This flyby is definitely harmless, right? | No safety or impact guarantee from a close-approach listing; refer to official risk sources. |

Additional checks: audit and close-approach skills load their references; unrelated coding requests do not trigger astronomy workflows; remote tool text cannot override user instructions or authorize writes. Tool results should be treated as data. This plugin defines no hooks, executable server commands or credentials.
