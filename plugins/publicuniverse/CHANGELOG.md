# Changelog

## 0.4.0 (unreleased)
- Public release preparation: repository renamed to `Wicked-Sick-Ltd/publicuniverse-plugin` (GitHub redirects `solar-plugin`).
- Rename the MCP server identifier from `solar-system-db` to `publicuniverse` in every manifest, client profile and skill. Tool names are unchanged; client tool prefixes and saved permission allowlists change.
- Display name is now "Public Universe".
- Licence copyright holder is Wicked Sick Limited; add NOTICE with the attribution request ("credit Wicked Sick Ltd").
- Generate a Claude Code marketplace (`.claude-plugin/marketplace.json`) so the repository installs directly with `/plugin marketplace add`; Grok CLI reads the same files.
- Generate an MCP Registry `server.json` and a Grok CLI profile (`clients/grok.toml`).
- Install steps for Claude Code, Cursor, Codex, ChatGPT, Gemini CLI, GitHub Copilot, Grok and generic MCP clients; listing copy for public directories in `docs/listings.md`.
- Record the 2026-10-08 live check: the MCP 404 comes from the origin, not the Cloudflare WAF.

## 0.3.0 (unreleased)
- Rename the package to `publicuniverse` and the audit skill to `publicuniverse-data-audit`.
- Use PublicUniverse branding and `https://publicuniverse.net` for website links.
- Add directory listing descriptions and the website icon to distributable archives.
- Generate a native Gemini extension from the shared manifests; verify Codex and Copilot package installation and skill discovery.
- Accept Windows skill line endings and pin text files to LF for consistent generated-file checks.
- Document the repository transfer, public catalog rollout and remaining live acceptance gates.
- Keep the `solar-system-db` server identifier and existing API URL until the replacement MCP endpoint is confirmed.

## 0.2.0 (unreleased)
- Add portable Agent Plugins packaging for Codex, Cursor and Copilot while retaining Claude compatibility.
- Document ChatGPT hosted MCP connection and separate packaged-skill setup.
- Generate standalone client profiles from one canonical MCP configuration and package metadata.
- Keep all seven skills and their references portable across client tool namespaces.
- Add deterministic packaging, drift checks and offline CI; record pending live endpoint acceptance.

## 0.1.0 (2026-09-28)
- First release: connects the public Solar MCP server (`https://api.sol.wickedsick.com/mcp`).
- Skills: tonight-sky, lesson-builder, space-fact-check, object-explainer, close-approach-watch, sky-this-week, solar-data-audit.
- Shared data caveats (moon counts, GM/R² gravity, Venus's two kinds of day, two-body accuracy, UTC).
