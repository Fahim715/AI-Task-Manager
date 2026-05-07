"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const onSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError("");
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      const data = await res.json();
      setError(data.error || "Login failed");
      return;
    }

    router.push("/dashboard");
  };

  return (
    <main className="min-h-screen flex items-center justify-center px-6">
      <div className="card w-full max-w-md p-8">
        <h1 className="text-3xl font-display font-semibold mb-4">Welcome back</h1>
        <p className="text-sm text-slate-600 mb-6">Log in to manage your org.</p>
        <form className="space-y-4" onSubmit={onSubmit}>
          <input
            className="w-full rounded-xl border border-slate-300 px-4 py-3"
            placeholder="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            className="w-full rounded-xl border border-slate-300 px-4 py-3"
            placeholder="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {error ? <p className="text-sm text-red-600">{error}</p> : null}
          <button className="w-full rounded-xl bg-ink text-white py-3">Log in</button>
        </form>
        <p className="text-sm text-slate-600 mt-6">
          New here? <Link className="underline" href="/register">Create an account</Link>
        </p>
      </div>
    </main>
  );
}
