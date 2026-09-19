import Link from "next/link";
import { prisma } from "@/lib/prisma";
import { CATEGORY_COLORS } from "@/lib/listings";

export const dynamic = "force-dynamic";

function CategoryBadge({ category }: { category: string }) {
  const classes =
    CATEGORY_COLORS[category as keyof typeof CATEGORY_COLORS] ??
    "bg-slate-100 text-slate-600";
  return (
    <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${classes}`}>
      {category}
    </span>
  );
}

export default async function HomePage() {
  const listings = await prisma.listing.findMany({
    orderBy: [{ featured: "desc" }, { createdAt: "desc" }]
  });

  return (
    <div className="space-y-12">
      <section className="rounded-3xl bg-gradient-to-br from-brand-600 to-brand-400 px-8 py-14 text-white shadow-lg">
        <p className="text-sm font-medium uppercase tracking-wide text-brand-100">
          The marketplace for AI tools & agents
        </p>
        <h1 className="mt-3 max-w-2xl text-4xl font-bold leading-tight sm:text-5xl">
          Find the right AI for the job — or ship your own.
        </h1>
        <p className="mt-4 max-w-xl text-brand-50">
          Browse a curated catalog of AI products from independent builders and
          teams. Publish your own tool in under a minute.
        </p>
        <div className="mt-8 flex gap-4">
          <Link
            href="/new"
            className="rounded-lg bg-white px-5 py-2.5 font-semibold text-brand-700 shadow-sm transition hover:bg-brand-50"
          >
            Publish a tool
          </Link>
          <a
            href="#catalog"
            className="rounded-lg border border-white/40 px-5 py-2.5 font-semibold text-white transition hover:bg-white/10"
          >
            Browse catalog
          </a>
        </div>
      </section>

      <section id="catalog" className="space-y-6">
        <div className="flex items-baseline justify-between">
          <h2 className="text-2xl font-semibold">
            Catalog
            <span className="ml-2 text-base font-normal text-slate-400">
              {listings.length} tools
            </span>
          </h2>
        </div>

        {listings.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center text-slate-500">
            No tools published yet.{" "}
            <Link href="/new" className="font-medium text-brand-600">
              Be the first to publish one.
            </Link>
          </div>
        ) : (
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {listings.map((listing) => (
              <article
                key={listing.id}
                className="flex flex-col rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:shadow-md"
              >
                <div className="flex items-center justify-between">
                  <CategoryBadge category={listing.category} />
                  {listing.featured && (
                    <span className="rounded-full bg-brand-50 px-2.5 py-0.5 text-xs font-medium text-brand-700">
                      ★ Featured
                    </span>
                  )}
                </div>
                <h3 className="mt-4 text-lg font-semibold">{listing.name}</h3>
                <p className="mt-1 text-sm font-medium text-slate-500">
                  {listing.tagline}
                </p>
                <p className="mt-3 flex-1 text-sm text-slate-600">
                  {listing.description}
                </p>
                <div className="mt-5 flex items-center justify-between border-t border-slate-100 pt-4 text-sm">
                  <span className="text-slate-500">by {listing.author}</span>
                  <span className="font-semibold text-brand-700">
                    {listing.pricing}
                  </span>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
