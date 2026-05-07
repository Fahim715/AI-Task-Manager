"use client";

import Link from "next/link";

export function Navbar() {
  return (
    <header className="flex items-center justify-between px-6 py-4 border-b border-slate-200 bg-white/70 backdrop-blur">
      <Link href="/" className="text-xl font-display font-semibold">TaskFlow AI</Link>
      <nav className="flex items-center gap-4 text-sm text-slate-600">
        <Link href="/dashboard">Overview</Link>
        <Link href="/dashboard/tasks">Tasks</Link>
        <Link href="/dashboard/invoices">Invoices</Link>
        <Link href="/dashboard/webhooks">Webhooks</Link>
        <Link href="/dashboard/settings">Settings</Link>
      </nav>
      <form action="/api/auth/logout" method="POST">
        <button className="px-4 py-2 rounded-full bg-ink text-white">Log out</button>
      </form>
    </header>
  );
}
