import type { WebhookLog } from "../lib/types";

interface WebhookLogTableProps {
  logs: WebhookLog[];
}

export function WebhookLogTable({ logs }: WebhookLogTableProps) {
  return (
    <div className="card overflow-hidden">
      <table className="w-full text-sm">
        <thead className="bg-slate-100 text-left">
          <tr>
            <th className="p-3">Event</th>
            <th className="p-3">Status</th>
            <th className="p-3">Delivered</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log) => (
            <tr key={log.id} className="border-t border-slate-200">
              <td className="p-3">{log.event}</td>
              <td className="p-3">{log.status_code ?? "pending"}</td>
              <td className="p-3">{new Date(log.delivered_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
