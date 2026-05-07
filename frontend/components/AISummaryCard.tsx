"use client";

import { useEffect, useRef, useState } from "react";
import { api } from "../lib/api";

export function AISummaryCard() {
  const [summary, setSummary] = useState("");
  const [display, setDisplay] = useState("");
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    let isMounted = true;
    api
      .getAISummary()
      .then((data) => {
        if (!isMounted) return;
        setSummary(data.summary || "No summary available.");
      })
      .catch(() => setSummary("AI summary unavailable."));

    return () => {
      isMounted = false;
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  useEffect(() => {
    if (!summary) return;
    const words = summary.split(" ");
    let index = 0;
    timerRef.current = setInterval(() => {
      index += 1;
      setDisplay(words.slice(0, index).join(" "));
      if (index >= words.length && timerRef.current) {
        clearInterval(timerRef.current);
      }
    }, 40);
  }, [summary]);

  return (
    <div className="card p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-slate-500">AI summary</p>
          <p className="text-lg font-display font-semibold">Org overview</p>
        </div>
        <span className="rounded-full bg-sky-100 px-3 py-1 text-xs text-sky-700">Live</span>
      </div>
      <p className="text-sm text-slate-600 mt-4 min-h-[80px]">{display || "Loading..."}</p>
    </div>
  );
}
