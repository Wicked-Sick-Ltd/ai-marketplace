import Link from "next/link";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { prisma } from "@/lib/prisma";
import { CATEGORIES, listingInputSchema, slugify } from "@/lib/listings";

async function createListing(formData: FormData) {
  "use server";

  const parsed = listingInputSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) {
    const [issue] = parsed.error.issues;
    redirect(`/new?error=${encodeURIComponent(issue.message)}`);
  }

  const data = parsed.data;
  const baseSlug = slugify(data.name) || "listing";
  let slug = baseSlug;
  let attempt = 1;
  while (await prisma.listing.findUnique({ where: { slug } })) {
    attempt += 1;
    slug = `${baseSlug}-${attempt}`;
  }

  await prisma.listing.create({ data: { ...data, slug } });

  revalidatePath("/");
  redirect("/");
}

export default async function NewListingPage({
  searchParams
}: {
  searchParams: Promise<{ error?: string }>;
}) {
  const { error } = await searchParams;

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="text-3xl font-bold">Publish a tool</h1>
      <p className="mt-2 text-slate-600">
        Add your AI product to the marketplace. It appears in the catalog
        instantly.
      </p>

      {error && (
        <div className="mt-6 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      <form action={createListing} className="mt-8 space-y-6">
        <Field label="Name">
          <input
            name="name"
            required
            placeholder="Atlas Copywriter"
            className="input"
          />
        </Field>

        <Field label="Tagline">
          <input
            name="tagline"
            required
            placeholder="On-brand marketing copy in seconds"
            className="input"
          />
        </Field>

        <Field label="Description">
          <textarea
            name="description"
            required
            rows={4}
            placeholder="What does your tool do and who is it for?"
            className="input"
          />
        </Field>

        <div className="grid gap-6 sm:grid-cols-2">
          <Field label="Category">
            <select name="category" className="input" defaultValue={CATEGORIES[0]}>
              {CATEGORIES.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </Field>

          <Field label="Pricing">
            <input name="pricing" required placeholder="$29/mo" className="input" />
          </Field>
        </div>

        <Field label="Author">
          <input
            name="author"
            required
            placeholder="Your team or company"
            className="input"
          />
        </Field>

        <div className="flex items-center gap-4 pt-2">
          <button
            type="submit"
            className="rounded-lg bg-brand-600 px-6 py-2.5 font-semibold text-white shadow-sm transition hover:bg-brand-700"
          >
            Publish tool
          </button>
          <Link href="/" className="text-sm font-medium text-slate-500 hover:text-slate-700">
            Cancel
          </Link>
        </div>
      </form>
    </div>
  );
}

function Field({
  label,
  children
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-sm font-medium text-slate-700">
        {label}
      </span>
      {children}
    </label>
  );
}
