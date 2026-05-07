"use client";

import { useEffect, useState } from "react";
import { InvoiceModal } from "../../../components/InvoiceModal";
import { api } from "../../../lib/api";
import type { Invoice } from "../../../lib/types";

export default function InvoicesPage() {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [open, setOpen] = useState(false);

  const load = async () => {
    const data = await api.listInvoices();
    setInvoices(data);
  };

  useEffect(() => {
    load().catch(() => setInvoices([]));
  }, []);

  const handleSave = async (payload: Partial<Invoice>) => {
    await api.createInvoice(payload);
    await load();
  };

  return (
    <section className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-display font-semibold">Invoices</h1>
        <button className="px-4 py-2 rounded-full bg-ink text-white" onClick={() => setOpen(true)}>
          New invoice
        </button>
      </div>

      <div className="card overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-100 text-left">
            <tr>
              <th className="p-3">Title</th>
              <th className="p-3">Amount</th>
              <th className="p-3">Status</th>
            </tr>
          </thead>
          <tbody>
            {invoices.map((invoice) => (
              <tr key={invoice.id} className="border-t border-slate-200">
                <td className="p-3">{invoice.title}</td>
                <td className="p-3">
                  {invoice.currency} {invoice.amount}
                </td>
                <td className="p-3">
                  <span className="rounded-full bg-slate-200 px-2 py-1 text-xs">
                    {invoice.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <InvoiceModal open={open} onClose={() => setOpen(false)} onSave={handleSave} />
    </section>
  );
}
