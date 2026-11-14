# Vendored copy: Public Universe plugin

Cursor team marketplaces resolve plugin sources as directories inside this catalogue repository, so this directory holds a copy of the Public Universe plugin package.

- Upstream: https://github.com/Wicked-Sick-Ltd/public-universe
- Version: 0.4.2
- Source commit: `8b1e7b348067194d5a400f6bf16a0144a51d74aa`, the head of [pull request 9](https://github.com/Wicked-Sick-Ltd/public-universe/pull/9) before it was squashed
- That pull request merged to `main` on 2026-11-12 as `f660a494163def6b3d9e4427eebcf9cf1190f052`. `main` on 2026-11-14 was `4d7fee039221247817b6ee7251a0a2970b6d66aa` (#10 stopped generating unused manifests; #11 updated the acceptance notes). This directory was not re-vendored to either SHA.
- Previous catalogue sync: 0.4.1 at `bb5919e47e8c8e1eb66c2fc5dcdba9bbc51b2f56`. Claude, Codex and Copilot indexes are still that 0.4.1 SHA. Its `mcp.json` advertises `https://api.sol.wickedsick.com/mcp`.
- Contents: the package files from that 0.4.2 commit, apart from three generated files this catalogue copy has omitted since 0.4.1 (`.codex-plugin/plugin.json`, `.plugin/plugin.json`, `mcp_config.json`). Advertised remote in this directory is `https://api.publicuniverse.net/mcp`. `https://api.sol.wickedsick.com/mcp` keeps working; the two hosts serve in parallel, with no redirect. `docs/listings.md` section 7 was edited in this catalogue so it no longer tells editors to pin 0.4.0.

Do not edit these files here. To update: build upstream at the reviewed commit, delete this directory's contents except this file, unzip the archive here and update the commit above. Claude, Codex and Copilot indexes stay on `bb5919e47e8c8e1eb66c2fc5dcdba9bbc51b2f56` until a catalogue change moves them. Cursor installs this directory.
