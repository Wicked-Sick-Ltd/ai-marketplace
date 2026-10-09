# Directory listing copy

Draft text for public directories. **Nothing here has been submitted.** Submit only after the repository is public and the live MCP check in [validation.md](validation.md) passes, because every directory below tests the server or the install.

## Shared facts

| Field | Value |
| --- | --- |
| Name / id | Public Universe / `publicuniverse` |
| Publisher | Wicked Sick Ltd (Wicked Sick Limited), hello@wickedsick.com |
| Website | https://publicuniverse.net |
| Repository | https://github.com/Wicked-Sick-Ltd/publicuniverse-plugin |
| Licence | MIT (please credit Wicked Sick Ltd; see NOTICE) |
| MCP endpoint | `https://api.sol.wickedsick.com/mcp` (Streamable HTTP, no auth); planned `https://api.publicuniverse.net/mcp` |
| Privacy policy | https://publicuniverse.net/privacy |
| Icon | `assets/icon.svg` |
| Category | Education (secondary: Science, Research) |
| Tags | astronomy, space, education, stargazing, solar-system, nasa, jpl, teachers, mcp, skills |

**One-liner (80 characters or fewer):** Free astronomy data and lesson-ready workflows for every AI agent.

**Short description (200 characters or fewer):** Explore 1.5 million solar system objects, plan a night's stargazing, build UK school lessons and fact-check space claims, using live catalogue data from the free Public Universe service.

**Long description:**

> Public Universe is a free, pro bono astronomy service from Wicked Sick Ltd. This plugin connects your agent to its public MCP server (no API key) and adds seven workflows: plan what to see tonight from any town, explain any planet, moon, asteroid or comet at a chosen reading level, build UK key-stage lessons and worksheets with live values, fact-check astronomy claims, track upcoming asteroid and comet close approaches, draft a sourced weekly sky roundup, and audit catalogue data against official sources. Data comes from NASA/JPL, the IAU Minor Planet Center and other public catalogues, with sources, units and retrieval dates kept in every answer. Read-only: it never writes data or controls telescopes. Astronomy, not astrology.

**Example prompts:** "What can I see tonight from Romsey?" / "Explain Saturn to a ten-year-old using live catalogue data." / "Make a Year 5 worksheet about the planets." / "Is Venus's day really longer than its year?" / "Which asteroids pass close to Earth this month?"

## 1. Claude plugin directory (first)

Submit the public repository URL through Anthropic's plugin directory submission form. The repository root has `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`; `claude plugin validate .` should pass.

- Plugin name: `publicuniverse`; marketplace name: `publicuniverse`
- Install test: `/plugin marketplace add https://github.com/Wicked-Sick-Ltd/publicuniverse-plugin.git` then `/plugin install publicuniverse@publicuniverse`
- Components: 7 skills, 1 remote HTTP MCP server; no hooks, commands, binaries or credentials
- Use the short and long descriptions above.

## 2. Cursor marketplace

Submit at https://cursor.com/marketplace/publish with the repository URL. The root `plugin.json`, `mcp.json` and `skills/` follow the Agent Plugins 1.0.0 format, which Cursor loads directly. Logo: `assets/icon.svg`. Description: short description above.

## 3. Official MCP Registry

`server.json` is generated at the repository root with the name `net.publicuniverse/publicuniverse`, which needs DNS verification of `publicuniverse.net`:

```sh
mcp-publisher login dns --domain publicuniverse.net --private-key <key>   # after adding the TXT record
mcp-publisher publish
```

Alternative without DNS: change the name to `io.github.wicked-sick-ltd/publicuniverse` and use `mcp-publisher login github`. The registry requires the remote URL to be publicly reachable, and each URL can belong to only one server name.

## 4. Smithery

Add an existing remote server at https://smithery.ai/new using the MCP URL (no authentication). Display name: Public Universe. Description: short description above. Smithery scans the tool list on submission, so do this after the endpoint works.

## 5. OpenAI / Codex plugin directory

Follow https://developers.openai.com/plugins/deploy/submission. The root `plugin.json` already carries the `com.openai` interface metadata (display name, descriptions, prompts, icon). Still needed from Wicked Sick: verified developer/business identity, domain verification, per-tool annotation justifications (all tools are read-only), support and terms URLs, a demo recording, and the five positive / three negative reviewer scenarios in [submission.md](submission.md).

## 6. Gemini CLI extensions gallery

The gallery indexes public GitHub repositories that contain `gemini-extension.json`. Add the repository topic `gemini-cli-extension` once public and check the listing at https://geminicli.com/extensions. Install line: `gemini extensions install https://github.com/Wicked-Sick-Ltd/publicuniverse-plugin`.

## 7. Wicked Sick catalogue (`Wicked-Sick-Ltd/ai-marketplace`)

Update the Claude, Codex and Copilot entries to the renamed repository and the merged 0.4.0 commit SHA, refresh the Gemini command, and add the Cursor entry (a vendored copy of this package at `plugins/publicuniverse/`, because Cursor team marketplaces resolve sources inside the catalogue repository).
