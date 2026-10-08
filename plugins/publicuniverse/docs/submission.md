# PublicUniverse public distribution

Release candidate: 0.4.0. The package is prepared for review, not approved for public-directory publication. Client evidence is recorded in [validation.md](validation.md).

## Identity and migration

- Package and client namespace: `publicuniverse`; display name: Public Universe.
- Repository: `Wicked-Sick-Ltd/publicuniverse-plugin` (rename of `solar-plugin`; GitHub keeps redirects from the old name for web, API and git URLs).
- Website: `https://publicuniverse.net`, matching the website repository's canonical deployment configuration.
- Audit skill: `publicuniverse-data-audit` replaces `solar-data-audit`. The other six skill names stay the same.
- MCP identifier: `publicuniverse` from 0.4.0 (was `solar-system-db`). Skills refer to the new identifier; tool names are unchanged.
- MCP URL: retain `https://api.sol.wickedsick.com/mcp` until the replacement is confirmed. It still returned 404 on 2026-10-08 (origin response, not a Cloudflare block); this blocks live acceptance on every host.
- Public catalog: `Wicked-Sick-Ltd/ai-marketplace`. Its Claude, Codex and Copilot indexes pin the plugin source revision; Gemini has an installation guide. Cursor imports the plugin source repository directly because this index does not vendor plugin directories.

Existing users should disable/remove the old `solar` plugin before enabling `publicuniverse`, using their client's plugin manager. Update explicit `/solar:…` invocations to `/publicuniverse:…` on Claude and any copied audit-skill directory after comparing local edits. Do not install both a full plugin and its standalone MCP profile, or overwrite unrelated client configuration.

## Repository and domain rollout

1. Rename the repository to `Wicked-Sick-Ltd/publicuniverse-plugin` (decision of 2026-10-08; a later transfer to the `public-universe` organisation remains possible and also keeps redirects).
2. Review the repository and its history for material unsuitable for public release; verify destination permissions. Make it public only after the transfer is complete.
3. Update `plugin.json.repository`, regenerate profiles and update every catalog source URL to the confirmed destination. Pin the reviewed package commit in all remote listings and the Gemini command.
4. Complete the website/domain and WAF rollout with the service owner. Update root `mcp.json` only with the confirmed endpoint and regenerate client profiles.
5. Repeat MCP initialization, tool discovery and representative read-only calls, then the client acceptance scenarios. Merge the catalog PR only when its source is anonymously accessible and live acceptance passes.

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
