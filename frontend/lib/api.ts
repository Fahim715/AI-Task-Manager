import type {
  AIInsightsResponse,
  AISummaryResponse,
  Invoice,
  Task,
  WebhookConfig,
  WebhookLog,
} from "./types";

const baseUrl = "/api/proxy";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${baseUrl}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },
  });

  if (!res.ok) {
    const data = await res.json().catch(() => ({ error: "Request failed" }));
    throw new Error(data.error || "Request failed");
  }

  return res.json() as Promise<T>;
}

export const api = {
  listTasks: (params = "") => request<Task[]>(`/tasks${params}`),
  createTask: (payload: Partial<Task>) =>
    request<Task>("/tasks/", { method: "POST", body: JSON.stringify(payload) }),
  updateTask: (id: number, payload: Partial<Task>) =>
    request<Task>(`/tasks/${id}`, { method: "PATCH", body: JSON.stringify(payload) }),
  deleteTask: (id: number) => request<{ message: string }>(`/tasks/${id}`, { method: "DELETE" }),

  listInvoices: () => request<Invoice[]>("/invoices/"),
  createInvoice: (payload: Partial<Invoice>) =>
    request<Invoice>("/invoices/", { method: "POST", body: JSON.stringify(payload) }),
  updateInvoice: (id: number, payload: Partial<Invoice>) =>
    request<Invoice>(`/invoices/${id}`, { method: "PATCH", body: JSON.stringify(payload) }),
  deleteInvoice: (id: number) =>
    request<{ message: string }>(`/invoices/${id}`, { method: "DELETE" }),

  listWebhooks: () => request<WebhookConfig[]>("/webhooks/"),
  createWebhook: (payload: Partial<WebhookConfig>) =>
    request<WebhookConfig>("/webhooks/", { method: "POST", body: JSON.stringify(payload) }),
  deleteWebhook: (id: number) =>
    request<{ message: string }>(`/webhooks/${id}`, { method: "DELETE" }),
  listWebhookLogs: () => request<WebhookLog[]>("/webhooks/logs"),

  getAISummary: () => request<AISummaryResponse>("/ai/summary"),
  getAIInsights: () => request<AIInsightsResponse>("/ai/insights"),
};
