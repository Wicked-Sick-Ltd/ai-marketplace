"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { CATEGORIES } from "@/lib/listings";

type FieldErrors = Record<string, string[] | undefined>;

export default function NewListingPage() {
  const router = useRouter();
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    setFieldErrors({});

    const formData = new FormData(event.currentTarget);
    const body = Object.fromEntries(formData.entries());

    const response = await fetch("/api/listings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    if (response.status === 201) {
      router.push("/");
      router.refresh();
      return;
    }

    const data = await response.json().catch(() => ({}));
    if (response.status === 422 && data?.details?.fieldErrors) {
      setFieldErrors(data.details.fieldErrors);
    }
    setError(data?.error ?? "Something went wrong. Please try again.");
    setSubmitting(false);
  }

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

      <form onSubmit={handleSubmit} className="mt-8 space-y-6">
        <Field label="Name" errors={fieldErrors.name}>
          <input
            name="name"
            required
            placeholder="Atlas Copywriter"
            className="input"
          />
        </Field>

        <Field label="Tagline" errors={fieldErrors.tagline}>
          <input
            name="tagline"
            required
            placeholder="On-brand marketing copy in seconds"
            className="input"
          />
        </Field>

        <Field label="Description" errors={fieldErrors.description}>
          <textarea
            name="description"
            required
            rows={4}
            placeholder="What does your tool do and who is it for?"
            className="input"
          />
        </Field>

        <div className="grid gap-6 sm:grid-cols-2">
          <Field label="Category" errors={fieldErrors.category}>
            <select name="category" className="input" defaultValue={CATEGORIES[0]}>
              {CATEGORIES.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </Field>

          <Field label="Pricing" errors={fieldErrors.pricing}>
            <input name="pricing" required placeholder="$29/mo" className="input" />
          </Field>
        </div>

        <Field label="Author" errors={fieldErrors.author}>
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
            disabled={submitting}
            className="rounded-lg bg-brand-600 px-6 py-2.5 font-semibold text-white shadow-sm transition hover:bg-brand-700 disabled:opacity-60"
          >
            {submitting ? "Publishing…" : "Publish tool"}
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
  errors,
  children
}: {
  label: string;
  errors?: string[];
  children: React.ReactNode;
}) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-sm font-medium text-slate-700">
        {label}
      </span>
      {children}
      {errors && errors.length > 0 && (
        <span className="mt-1 block text-xs text-red-600">{errors[0]}</span>
      )}
    </label>
  );
}
