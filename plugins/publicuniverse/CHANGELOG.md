# Changelog

All notable changes to this plugin are documented here.

## [Unreleased]

## 0.4.1 (2026-10-16)

### Added

- Cursor marketplace manifest (`.cursor-plugin/plugin.json`), generated from `plugin.json` with category `education`, logo, keywords and MCP/skills paths.

### Changed

- README and submission docs reflect a live public MCP endpoint (verified 2026-10-16) and a public `Wicked-Sick-Ltd/public-universe` repository.
- [validation.md](docs/validation.md) records full initialize, tool-list and sample tool-call evidence.

## 0.4.0 (2026-10-09)

First public release as **Public Universe** (`publicuniverse`). It also ships the
0.2.0 and 0.3.0 changes below, which were never tagged separately. Based on
`main` at `4544cb4772277805d90aeefb0c1601402c893979`.

### Added
- Claude Code marketplace (`.claude-plugin/marketplace.json`), which Grok CLI also reads, an MCP Registry `server.json` and a Grok CLI profile (`clients/grok.toml`) (#3).
- Install steps for Claude Code, Cursor, Codex, ChatGPT, Gemini CLI, GitHub Copilot, Grok and generic MCP clients, plus draft directory listing copy in `docs/listings.md` (nothing submitted) (#3).
- `NOTICE` asking reusers to credit "Wicked Sick Ltd" (#3).
- Native Gemini extension and portable Agent Plugins packaging for Codex, Cursor and Copilot, generated from shared manifests, with drift checks and offline CI (#1, #2).

### Changed
- **Breaking for existing installs:** the MCP server identifier is now `publicuniverse` instead of `solar-system-db` in every manifest, client profile and skill. Tool names are unchanged, but client tool prefixes and saved permission allowlists change (#3).
- Display name is "Public Universe"; the audit skill is now `publicuniverse-data-audit` (#2, #3).
- Licence copyright holder is Wicked Sick Limited; licence remains MIT (#3).
- Repository metadata now points at `Wicked-Sick-Ltd/publicuniverse-plugin` (#3).

### Known limitations
- The repository has **not** been renamed yet: it is still `Wicked-Sick-Ltd/solar-plugin`, so install commands and links that use `publicuniverse-plugin` return 404 until the rename happens. #3 asked for the rename before merge.
- The remote MCP endpoint (`https://api.sol.wickedsick.com/mcp`) still returns 404 from the API origin, so live tool calls do not work yet. Skills install and load. The 8 October check showed the 404 comes from the origin, not the Cloudflare WAF (#3).
- `https://api.publicuniverse.net/mcp` is planned but not live; the package keeps the current URL until it is.
- The repository is internal, so public install routes need it to be made public first.

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
