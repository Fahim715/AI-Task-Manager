"use client";

import { useEffect, useState } from "react";
import { AISummaryCard } from "../../components/AISummaryCard";
import { StatCard } from "../../components/StatCard";
import { api } from "../../lib/api";

export default function DashboardPage() {
  const [taskCount, setTaskCount] = useState(0);
  const [invoiceCount, setInvoiceCount] = useState(0);
  const [insights, setInsights] = useState("Loading insights...");

  useEffect(() => {
    api.listTasks("?limit=200")
      .then((tasks) => setTaskCount(tasks.length))
      .catch(() => setTaskCount(0));
    api.listInvoices()
      .then((invoices) => setInvoiceCount(invoices.length))
      .catch(() => setInvoiceCount(0));
    api.getAIInsights()
      .then((data) => setInsights(data.summary))
      .catch(() => setInsights("AI insights unavailable."));
  }, []);

  return (
    <div className="space-y-8">
      <div className="grid gap-4 md:grid-cols-3">
        <StatCard title="Tasks" value={String(taskCount)} hint="Across all boards" />
        <StatCard title="Invoices" value={String(invoiceCount)} hint="Tracked this month" />
        <StatCard title="Alerts" value="3" hint="Overdue follow-ups" />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <AISummaryCard />
        <div className="card p-6">
          <p className="text-xs uppercase tracking-[0.2em] text-slate-500">AI insights</p>
          <p className="text-lg font-display font-semibold mt-2">Weekly pulse</p>
          <p className="text-sm text-slate-600 mt-4">{insights}</p>
        </div>
      </div>
    </div>
  );
}
