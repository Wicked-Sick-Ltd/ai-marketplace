import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Marketplace",
  description: "Discover, compare, and publish AI tools and agents."
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <header className="border-b border-slate-200 bg-white/80 backdrop-blur">
          <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
            <Link href="/" className="flex items-center gap-2 font-semibold">
              <span className="grid h-8 w-8 place-items-center rounded-lg bg-brand-600 text-white">
                ▲
              </span>
              <span className="text-lg">AI Marketplace</span>
            </Link>
            <nav className="flex items-center gap-6 text-sm font-medium text-slate-600">
              <Link href="/" className="hover:text-brand-600">
                Browse
              </Link>
              <Link
                href="/new"
                className="rounded-lg bg-brand-600 px-4 py-2 text-white shadow-sm transition hover:bg-brand-700"
              >
                Publish a tool
              </Link>
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-6 py-10">{children}</main>
        <footer className="mx-auto max-w-6xl px-6 py-10 text-sm text-slate-400">
          Built as a Cloud Agent environment demo · AI Marketplace
        </footer>
      </body>
    </html>
  );
}
