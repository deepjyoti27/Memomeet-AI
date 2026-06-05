import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MemoMeet AI — Enterprise Truth & Commitment Intelligence",
  description:
    "The system of record for what was promised, decided, and agreed across every customer conversation.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-background font-sans text-foreground antialiased">
        {children}
      </body>
    </html>
  );
}
