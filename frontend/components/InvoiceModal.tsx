"use client";

import { useEffect, useState } from "react";
import type { Invoice } from "../lib/types";

interface InvoiceModalProps {
  open: boolean;
  initial?: Partial<Invoice>;
  onClose: () => void;
  onSave: (payload: Partial<Invoice>) => void;
}

export function InvoiceModal({ open, initial, onClose, onSave }: InvoiceModalProps) {
  const [title, setTitle] = useState(initial?.title || "");
  const [amount, setAmount] = useState(initial?.amount?.toString() || "");
  const [currency, setCurrency] = useState(initial?.currency || "BDT");

  useEffect(() => {
    if (!open) return;
    setTitle(initial?.title || "");
    setAmount(initial?.amount?.toString() || "");
    setCurrency(initial?.currency || "BDT");
  }, [open, initial]);

  if (!open) return null;

  const handleSave = () => {
    onSave({ title, amount: Number(amount), currency });
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 px-4">
      <div className="card w-full max-w-md p-6">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-display font-semibold">Invoice</h2>
          <button onClick={onClose} className="text-slate-500">Close</button>
        </div>
        <div className="mt-4 space-y-3">
          <input
            className="w-full rounded-xl border border-slate-300 px-4 py-2"
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          <input
            className="w-full rounded-xl border border-slate-300 px-4 py-2"
            placeholder="Amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
          />
          <input
            className="w-full rounded-xl border border-slate-300 px-4 py-2"
            placeholder="Currency"
            value={currency}
            onChange={(e) => setCurrency(e.target.value)}
          />
        </div>
        <button onClick={handleSave} className="mt-6 w-full rounded-xl bg-ink text-white py-2">
          Save
        </button>
      </div>
    </div>
  );
}
