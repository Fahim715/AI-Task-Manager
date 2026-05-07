interface StatCardProps {
  title: string;
  value: string;
  hint: string;
}

export function StatCard({ title, value, hint }: StatCardProps) {
  return (
    <div className="card p-5">
      <p className="text-xs uppercase tracking-[0.2em] text-slate-500">{title}</p>
      <p className="text-3xl font-display font-semibold mt-2">{value}</p>
      <p className="text-sm text-slate-500 mt-2">{hint}</p>
    </div>
  );
}
