export type TaskStatus = "todo" | "in_progress" | "done";
export type InvoiceStatus = "draft" | "sent" | "paid";

export interface Task {
  id: number;
  title: string;
  description?: string | null;
  status: TaskStatus;
  due_date?: string | null;
  overdue: boolean;
  org_id: number;
  assignee_id?: number | null;
}

export interface Invoice {
  id: number;
  title: string;
  amount: number;
  currency: string;
  status: InvoiceStatus;
  task_id?: number | null;
  org_id: number;
}

export interface WebhookConfig {
  id: number;
  org_id: number;
  url: string;
  events: string[];
  is_active: boolean;
}

export interface WebhookLog {
  id: number;
  webhook_config_id: number;
  event: string;
  payload: Record<string, unknown>;
  status_code?: number | null;
  delivered_at: string;
}

export interface AISummaryResponse {
  summary: string;
}

export interface AIInsightsResponse {
  summary: string;
}
