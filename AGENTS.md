# Agent instructions

This repository is an **index**. It lists plugins; it does not contain plugin code.

- Do not vendor plugin sources here.
- Pin every remote plugin to a full 40-character commit SHA.
- List a plugin only on the catalogs where it has a real runtime.
- `token-usage` stays on the Claude index until other hosts have a parser or an honest "Claude transcripts only" listing.
- After catalog edits, run `python3 scripts/validate.py`.

Product-repo agent rules (Forge, Yaegi, Traefik) live in those repos, not here.
