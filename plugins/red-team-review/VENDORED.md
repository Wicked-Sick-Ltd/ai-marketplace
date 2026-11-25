# Published copy: red-team-review

This directory is the public package and the canonical source. Claude, Cursor,
Codex, Copilot and Gemini install it from `Wicked-Sick-Ltd/ai-marketplace`.
Their catalog entries point here.

Provenance: first-party package published in this repository. There is no separate upstream pin.

- Version on every manifest and on the Claude, Cursor and Copilot catalog entries: `1.0.0`. The Codex catalog entry has no version field.
- The skill text in this directory is the published copy.
- `.codex-plugin/plugin.json` is the Codex manifest. `.plugin/plugin.json` is the manifest Copilot CLI reads first. `.github/plugin/plugin.json` is the same manifest. `.cursor-plugin/plugin.json` is the Cursor manifest. `.claude-plugin/plugin.json` is the Claude manifest. `plugin.json` and `gemini-extension.json` are the Antigravity / Gemini manifests.
