"use client";

import { useEffect, useState } from "react";
import { api } from "../../../lib/api";
import { WebhookLogTable } from "../../../components/WebhookLogTable";
import type { WebhookConfig, WebhookLog } from "../../../lib/types";

const defaultEvents = ["task.created", "task.updated", "task.deleted", "invoice.paid"];

export default function WebhooksPage() {
  const [hooks, setHooks] = useState<WebhookConfig[]>([]);
  const [logs, setLogs] = useState<WebhookLog[]>([]);
  const [url, setUrl] = useState("");
  const [secret, setSecret] = useState("");
  const [events, setEvents] = useState<string[]>(["task.created"]);

  const load = async () => {
    setHooks(await api.listWebhooks());
    setLogs(await api.listWebhookLogs());
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  const toggleEvent = (value: string) => {
    setEvents((prev) =>
      prev.includes(value) ? prev.filter((evt) => evt !== value) : [...prev, value]
    );
  };

  const handleCreate = async () => {
    await api.createWebhook({ url, secret, events, is_active: true });
    setUrl("");
    setSecret("");
    setEvents(["task.created"]);
    await load();
  };

  return (
    <section className="space-y-6">
      <h1 className="text-2xl font-display font-semibold">Webhooks</h1>

      <div className="card p-5 space-y-4">
        <div className="grid gap-3 md:grid-cols-2">
          <input
            className="rounded-xl border border-slate-300 px-4 py-2"
            placeholder="Webhook URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <input
            className="rounded-xl border border-slate-300 px-4 py-2"
            placeholder="Secret"
            value={secret}
            onChange={(e) => setSecret(e.target.value)}
          />
        </div>
        <div className="flex flex-wrap gap-2">
          {defaultEvents.map((event) => (
            <button
              key={event}
              type="button"
              className={`px-3 py-1 rounded-full text-xs border ${
                events.includes(event) ? "bg-ink text-white" : "bg-white"
              }`}
              onClick={() => toggleEvent(event)}
            >
              {event}
            </button>
          ))}
        </div>
        <button className="px-4 py-2 rounded-full bg-ink text-white" onClick={handleCreate}>
          Add webhook
        </button>
      </div>

      <div className="card p-5">
        <h2 className="text-lg font-display font-semibold mb-4">Active webhooks</h2>
        <div className="space-y-3">
          {hooks.map((hook) => (
            <div key={hook.id} className="flex items-center justify-between">
              <div>
                <p className="font-semibold">{hook.url}</p>
                <p className="text-xs text-slate-500">{hook.events.join(", ")}</p>
              </div>
              <button
                className="text-sm text-red-600"
                onClick={async () => {
                  await api.deleteWebhook(hook.id);
                  await load();
                }}
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h2 className="text-lg font-display font-semibold mb-4">Delivery logs</h2>
        <WebhookLogTable logs={logs} />
      </div>
    </section>
  );
}
