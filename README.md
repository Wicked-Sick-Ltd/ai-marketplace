# Wicked Sick AI marketplace

GitHub catalogs for the agent plugins we actually install. Plugins are **not** vendored here; each index points at a source repo, pinned by commit SHA.

This is not a Traefik module and not a substitute for `CLAUDE.md` / `AGENTS.md` in product repos. See the plan in [traefik-laravel-forge](https://github.com/Wicked-Sick-Ltd/traefik-laravel-forge/blob/master/docs/cross-ai-marketplace-plan.md).

## Add the marketplace

```bash
# Claude Code (Grok Build reads this catalog too)
claude plugin marketplace add Wicked-Sick-Ltd/ai-marketplace

# ChatGPT Work / Codex CLI
codex plugin marketplace add Wicked-Sick-Ltd/ai-marketplace --sparse .agents/plugins
```

- **Cursor:** Teams or Enterprise → marketplace → connect this GitHub repository.
- **Copilot:** `"chat.plugins.marketplaces": ["Wicked-Sick-Ltd/ai-marketplace"]`
- **Gemini CLI:** no catalog file. Install from the plugin repo: see [`gemini/README.md`](gemini/README.md).
- **Grok:** add the Claude marketplace above. A Grok-native index is omitted on purpose.

Then install individual plugins (Claude):

```bash
claude plugin install token-usage@wickedsick
```

## Indexes

| Client | File | Plugins listed today |
| --- | --- | --- |
| Claude Code / Grok | `.claude-plugin/marketplace.json` | `token-usage` (pinned) |
| Cursor | `.cursor-plugin/marketplace.json` | none yet |
| ChatGPT / Codex | `.agents/plugins/marketplace.json` | none yet |
| Copilot | `.github/plugin/marketplace.json` | none yet |
| Gemini | [`gemini/README.md`](gemini/README.md) | none yet |

`token-usage` is Claude-only until it can parse that host's session logs (or the listing is explicitly "Claude transcripts only"). Workflow skills can be added to every Agent Skills catalog.

## Horses for courses

| Job | Default agent |
| --- | --- |
| Day-to-day coding, Cloud Agents | Cursor |
| Claude-native plugins, Cowork, hooks | Claude Code |
| ChatGPT app / native CLI | ChatGPT Work + Codex CLI |
| VS Code, PRs | Copilot |
| Gemini CLI / Google-shaped work | Gemini |
| Terminal agent that can reuse Claude plugins | Grok |

## Add a plugin

1. Keep the plugin in its own repository.
2. Pin a **full 40-character commit SHA** (and a tag `ref` when one exists). Do not float on `main`.
3. List it only on marketplaces where it has a real runtime.
4. Run `python3 scripts/validate.py`.

Owner: Wicked Sick Ltd (`craig@wickedsick.com`).
# ai-marketplace

A marketplace for AI tools and agents. Browse a curated catalog of AI products
and publish your own. Built with Next.js (App Router), TypeScript, Tailwind CSS,
and Prisma with SQLite so the whole stack runs locally with no external
services.

## Tech stack

- **Next.js 14** (App Router) + **React 18** + **TypeScript**
- **Tailwind CSS** for styling
- **Prisma ORM** backed by **SQLite** (file-based, zero external dependencies)
- **Zod** for request validation

## Getting started

Requires Node.js 20+ (this repo is developed on Node 22).

```bash
npm install
npx prisma generate          # generate the Prisma client
npx prisma migrate deploy    # apply migrations (creates prisma/dev.db)
npm run db:seed              # load sample listings (idempotent)
npm run dev                  # start the dev server on http://localhost:3000
```

Then open http://localhost:3000.

## Common commands

| Command | Description |
| --- | --- |
| `npm run dev` | Start the Next.js dev server on port 3000 |
| `npm run build` | Create a production build |
| `npm run start` | Serve the production build |
| `npm run lint` | Run ESLint (`next lint`) |
| `npm run typecheck` | Type-check with `tsc --noEmit` |
| `npm run db:migrate` | Apply pending migrations (`prisma migrate deploy`) |
| `npm run db:seed` | Seed sample listings (safe to re-run) |

## API

- `GET /api/listings` — list all listings (featured first).
- `POST /api/listings` — create a listing. JSON body validated with Zod:
  `{ name, tagline, description, category, pricing, author }`.

## Project layout

```
prisma/
  schema.prisma      # Listing model (SQLite)
  seed.ts            # idempotent sample data
  migrations/        # committed migration history
src/
  app/
    page.tsx         # catalog (browse listings)
    new/page.tsx     # publish-a-tool form
    api/listings/    # REST endpoints (GET, POST)
    layout.tsx
    globals.css
  lib/
    prisma.ts        # Prisma client singleton
    listings.ts      # shared validation + helpers
```

## Cloud Agent environment

`.cursor/environment.json` configures the Cloud Agent environment: `install`
installs dependencies, generates the Prisma client, applies migrations, and
seeds sample data; the `dev` terminal runs `npm run dev` on port 3000.
