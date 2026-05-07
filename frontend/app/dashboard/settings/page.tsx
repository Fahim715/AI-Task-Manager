"use client";

import { useState } from "react";

export default function SettingsPage() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const invite = async () => {
    setMessage("");
    const res = await fetch("/api/auth/invite", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });

    if (!res.ok) {
      const data = await res.json();
      setMessage(data.error || "Invite failed");
      return;
    }

    setMessage("Invite sent.");
    setEmail("");
  };

  return (
    <section className="space-y-6">
      <h1 className="text-2xl font-display font-semibold">Settings</h1>

      <div className="card p-5 space-y-4">
        <h2 className="text-lg font-display font-semibold">Invite teammates</h2>
        <input
          className="w-full rounded-xl border border-slate-300 px-4 py-2"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        {message ? <p className="text-sm text-slate-600">{message}</p> : null}
        <button className="px-4 py-2 rounded-full bg-ink text-white" onClick={invite}>
          Send invite
        </button>
      </div>
    </section>
  );
}
