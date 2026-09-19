import { z } from "zod";

export const CATEGORY_COLORS = {
  Writing: "bg-amber-100 text-amber-700",
  Image: "bg-pink-100 text-pink-700",
  Support: "bg-emerald-100 text-emerald-700",
  Analytics: "bg-sky-100 text-sky-700",
  Productivity: "bg-violet-100 text-violet-700",
  "Developer Tools": "bg-slate-200 text-slate-700"
} as const;

export const CATEGORIES = Object.keys(CATEGORY_COLORS) as [
  keyof typeof CATEGORY_COLORS,
  ...(keyof typeof CATEGORY_COLORS)[]
];

export const listingInputSchema = z.object({
  name: z.string().trim().min(2, "Name must be at least 2 characters").max(80),
  tagline: z.string().trim().min(4, "Tagline is too short").max(120),
  description: z
    .string()
    .trim()
    .min(20, "Description must be at least 20 characters")
    .max(1000),
  category: z.enum(CATEGORIES),
  pricing: z.string().trim().min(1, "Pricing is required").max(40),
  author: z.string().trim().min(2, "Author is required").max(80)
});

export function slugify(value: string): string {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 60);
}
