"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { useMemo, useState } from "react";
import Link from "next/link";

export default function RegisterPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const inviteToken = useMemo(() => searchParams.get("token"), [searchParams]);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [orgName, setOrgName] = useState("");
  const [error, setError] = useState("");

  const onSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError("");

    const endpoint = inviteToken ? "/api/auth/accept-invite" : "/api/auth/register";
    const body = inviteToken
      ? { token: inviteToken, password }
      : { email, password, org_name: orgName };

    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      const data = await res.json();
      setError(data.error || "Registration failed");
      return;
    }

    router.push("/dashboard");
  };

  return (
    <main className="min-h-screen flex items-center justify-center px-6">
      <div className="card w-full max-w-md p-8">
        <h1 className="text-3xl font-display font-semibold mb-4">
          {inviteToken ? "Join your org" : "Create your workspace"}
        </h1>
        <p className="text-sm text-slate-600 mb-6">
          {inviteToken
            ? "You have been invited to TaskFlow AI. Set a password to join."
            : "Start a new organization in minutes."}
        </p>
        <form className="space-y-4" onSubmit={onSubmit}>
          {!inviteToken ? (
            <>
              <input
                className="w-full rounded-xl border border-slate-300 px-4 py-3"
                placeholder="Org name"
                value={orgName}
                onChange={(e) => setOrgName(e.target.value)}
              />
              <input
                className="w-full rounded-xl border border-slate-300 px-4 py-3"
                placeholder="Email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </>
          ) : null}
          <input
            className="w-full rounded-xl border border-slate-300 px-4 py-3"
            placeholder="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {error ? <p className="text-sm text-red-600">{error}</p> : null}
          <button className="w-full rounded-xl bg-ink text-white py-3">
            {inviteToken ? "Accept invite" : "Create account"}
          </button>
        </form>
        <p className="text-sm text-slate-600 mt-6">
          Already have access? <Link className="underline" href="/login">Log in</Link>
        </p>
      </div>
    </main>
  );
}
