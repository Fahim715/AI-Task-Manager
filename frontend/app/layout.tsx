import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "TaskFlow AI",
  description: "AI-powered task and invoice management for modern teams.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="gradient-bg min-h-screen">{children}</body>
    </html>
  );
}
