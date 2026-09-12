import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

const listings = [
  {
    slug: "atlas-copywriter",
    name: "Atlas Copywriter",
    tagline: "On-brand marketing copy in seconds",
    description:
      "Atlas learns your brand voice from a few examples and drafts landing pages, ads, and email campaigns that stay consistent across every channel.",
    category: "Writing",
    pricing: "$29/mo",
    author: "Northwind Labs",
    featured: true
  },
  {
    slug: "pixel-forge",
    name: "Pixel Forge",
    tagline: "Text-to-image generation for product teams",
    description:
      "Generate production-ready hero images, icons, and illustrations with fine-grained style controls and a built-in brand kit.",
    category: "Image",
    pricing: "$49/mo",
    author: "Forge Studio",
    featured: true
  },
  {
    slug: "quorum-support",
    name: "Quorum Support",
    tagline: "An AI teammate for your help desk",
    description:
      "Quorum resolves tier-1 tickets automatically, drafts replies for agents, and surfaces the docs your customers actually need.",
    category: "Support",
    pricing: "$99/mo",
    author: "Quorum AI",
    featured: false
  },
  {
    slug: "ledger-sense",
    name: "Ledger Sense",
    tagline: "Natural-language analytics for finance",
    description:
      "Ask questions about revenue, burn, and runway in plain English and get charts, forecasts, and board-ready summaries.",
    category: "Analytics",
    pricing: "$149/mo",
    author: "Sense Data",
    featured: false
  },
  {
    slug: "scribe-transcribe",
    name: "Scribe",
    tagline: "Meeting transcription and action items",
    description:
      "Scribe joins your calls, produces accurate transcripts, and turns every meeting into a tidy list of decisions and follow-ups.",
    category: "Productivity",
    pricing: "Free",
    author: "Scribe Inc.",
    featured: false
  },
  {
    slug: "sentinel-review",
    name: "Sentinel Review",
    tagline: "Automated code review that catches real bugs",
    description:
      "Sentinel reviews pull requests for security issues, logic errors, and style violations, leaving inline comments your team can act on.",
    category: "Developer Tools",
    pricing: "$39/mo",
    author: "Sentinel Systems",
    featured: true
  }
];

async function main() {
  for (const listing of listings) {
    await prisma.listing.upsert({
      where: { slug: listing.slug },
      update: listing,
      create: listing
    });
  }
  const count = await prisma.listing.count();
  console.log(`Seed complete. ${count} listings in the marketplace.`);
}

main()
  .catch((error) => {
    console.error(error);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
