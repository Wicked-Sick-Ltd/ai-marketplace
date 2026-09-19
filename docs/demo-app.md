# Local demo app

A small Next.js listings app that lives in this tree so the Cursor Cloud Agent
environment (`.cursor/environment.json`) has something to install and run. It is
**not** plugin source, and its listings are **not** the plugin catalogs — those
are the JSON indexes described in the [README](../README.md) and validated by
`python3 scripts/validate.py`.

CI (`.github/workflows/validate.yml`) runs the Python catalog checks only. The
demo app's lint, typecheck, and build are unenforced; run them locally.

## Tech stack

- **Next.js 15** (App Router) + **React 18** + **TypeScript**
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
Local config comes from `.env`, which is git-ignored — copy `.env.example`
(a SQLite `DATABASE_URL`) to get started; the Cloud Agent install does this.
