import "./globals.css";
import { Navigation } from "@/components/Navigation";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Fleetos — Agentic Multimodal Fleet Intelligence Platform",
  description: "Fleetos is a logistics control system that does not just plan the route — it keeps the fleet optimized when reality changes.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 text-slate-900 antialiased">
        <Navigation />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
      </body>
    </html>
  );
}
