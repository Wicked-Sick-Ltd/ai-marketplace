# Vendored copy: Public Universe plugin

Cursor team marketplaces resolve plugin sources as directories inside this catalogue repository, so this directory holds a copy of the Public Universe plugin package.

- Upstream: https://github.com/Wicked-Sick-Ltd/public-universe
- Version: 0.4.2
- Source commit: `8b1e7b348067194d5a400f6bf16a0144a51d74aa` (head of [pull request 9](https://github.com/Wicked-Sick-Ltd/public-universe/pull/9), not yet on `main`)
- Previous catalogue sync: 0.4.1 at `bb5919e47e8c8e1eb66c2fc5dcdba9bbc51b2f56`
- Contents: the package files from that 0.4.2 commit, apart from three generated files this catalogue copy has omitted since 0.4.1 (`.codex-plugin/plugin.json`, `.plugin/plugin.json`, `mcp_config.json`). Advertised remote is `https://api.publicuniverse.net/mcp`. `https://api.sol.wickedsick.com/mcp` keeps working; the two hosts serve in parallel, with no redirect.

Do not edit these files here. To update: build upstream at the reviewed commit, delete this directory's contents except this file, unzip the archive here and update the commit above. Claude, Codex and Copilot indexes stay on the merged `main` SHA until pull request 9 merges; Cursor installs this directory.
