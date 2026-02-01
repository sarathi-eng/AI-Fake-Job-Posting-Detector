import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "AI Fake Job Posting Detector",
  description:
    "Detect fake job posts across platforms using AI with explainable risk scoring.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
