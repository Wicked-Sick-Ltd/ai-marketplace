import { z } from "zod";

export const CATEGORIES = [
  "Writing",
  "Image",
  "Support",
  "Analytics",
  "Productivity",
  "Developer Tools"
] as const;

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

export type ListingInput = z.infer<typeof listingInputSchema>;

export function slugify(value: string): string {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 60);
}
