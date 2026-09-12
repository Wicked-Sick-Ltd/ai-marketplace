import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { listingInputSchema, slugify } from "@/lib/listings";

export const dynamic = "force-dynamic";

export async function GET() {
  const listings = await prisma.listing.findMany({
    orderBy: [{ featured: "desc" }, { createdAt: "desc" }]
  });
  return NextResponse.json({ listings });
}

export async function POST(request: Request) {
  let payload: unknown;
  try {
    payload = await request.json();
  } catch {
    return NextResponse.json(
      { error: "Request body must be valid JSON." },
      { status: 400 }
    );
  }

  const parsed = listingInputSchema.safeParse(payload);
  if (!parsed.success) {
    return NextResponse.json(
      { error: "Validation failed", details: parsed.error.flatten() },
      { status: 422 }
    );
  }

  const data = parsed.data;
  const baseSlug = slugify(data.name) || "listing";
  let slug = baseSlug;
  let attempt = 1;
  while (await prisma.listing.findUnique({ where: { slug } })) {
    attempt += 1;
    slug = `${baseSlug}-${attempt}`;
  }

  const listing = await prisma.listing.create({
    data: { ...data, slug }
  });

  return NextResponse.json({ listing }, { status: 201 });
}
