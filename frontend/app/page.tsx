import Link from "next/link";

export default function LandingPage() {
  return (
    <main className="px-6 py-12">
      <section className="mx-auto max-w-6xl">
        <nav className="flex items-center justify-between mb-16">
          <div className="text-2xl font-display font-semibold">TaskFlow AI</div>
          <div className="flex gap-4 text-sm">
            <Link href="/login" className="px-4 py-2 rounded-full border border-slate-300">
              Log in
            </Link>
            <Link
              href="/register"
              className="px-4 py-2 rounded-full bg-ink text-white shadow"
            >
              Get started
            </Link>
          </div>
        </nav>

        <div className="grid gap-10 lg:grid-cols-2 items-center">
          <div className="space-y-6">
            <p className="text-sm uppercase tracking-[0.3em] text-slate-500">TaskFlow AI</p>
            <h1 className="text-5xl font-display font-bold leading-tight text-ink">
              Run your team&apos;s tasks and invoices with an AI co-pilot.
            </h1>
            <p className="text-lg text-slate-600">
              Multi-tenant workspace, real-time webhooks, and automated insights for ops
              teams who ship fast.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link
                href="/register"
                className="px-6 py-3 rounded-full bg-ink text-white shadow-lg"
              >
                Start free
              </Link>
              <Link
                href="/login"
                className="px-6 py-3 rounded-full border border-slate-300"
              >
                View dashboard
              </Link>
            </div>
          </div>

          <div className="card p-8 space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-500">AI Highlights</p>
                <p className="text-2xl font-display font-semibold">Weekly Momentum</p>
              </div>
              <span className="px-3 py-1 text-xs rounded-full bg-sky-100 text-sky-700">Live</span>
            </div>
            <ul className="space-y-3 text-sm text-slate-600">
              <li className="flex items-center justify-between">
                <span>Tasks completed</span>
                <span className="font-semibold text-ink">42</span>
              </li>
              <li className="flex items-center justify-between">
                <span>Invoices paid</span>
                <span className="font-semibold text-ink">BDT 128k</span>
              </li>
              <li className="flex items-center justify-between">
                <span>Webhooks delivered</span>
                <span className="font-semibold text-ink">312</span>
              </li>
            </ul>
            <div className="rounded-2xl bg-slate-900 text-white p-5">
              <p className="text-xs uppercase text-slate-400">AI summary</p>
              <p className="text-sm">
                Team velocity improved by 18%. Finance ops cleared overdue invoices in
                record time.
              </p>
            </div>
          </div>
        </div>

        <section className="grid gap-6 md:grid-cols-3 mt-20">
          {[
            {
              title: "Smart task ops",
              body: "AI suggestions, overdue alerts, and assignee load balancing.",
            },
            {
              title: "Invoice mastery",
              body: "Track invoice status, tie work to revenue, and export quick summaries.",
            },
            {
              title: "Webhook automation",
              body: "Notify downstream systems instantly with HMAC-signed webhooks.",
            },
          ].map((item) => (
            <div key={item.title} className="card p-6">
              <h3 className="font-display text-xl mb-2">{item.title}</h3>
              <p className="text-sm text-slate-600">{item.body}</p>
            </div>
          ))}
        </section>
      </section>
    </main>
  );
}
