"use client";

import { createContext, useContext, useReducer } from "react";
import type { Invoice, Task, WebhookConfig, WebhookLog } from "../types";

interface AppState {
  tasks: Task[];
  invoices: Invoice[];
  webhooks: WebhookConfig[];
  webhookLogs: WebhookLog[];
}

type Action =
  | { type: "set_tasks"; payload: Task[] }
  | { type: "set_invoices"; payload: Invoice[] }
  | { type: "set_webhooks"; payload: WebhookConfig[] }
  | { type: "set_webhook_logs"; payload: WebhookLog[] };

const initialState: AppState = {
  tasks: [],
  invoices: [],
  webhooks: [],
  webhookLogs: [],
};

function reducer(state: AppState, action: Action): AppState {
  switch (action.type) {
    case "set_tasks":
      return { ...state, tasks: action.payload };
    case "set_invoices":
      return { ...state, invoices: action.payload };
    case "set_webhooks":
      return { ...state, webhooks: action.payload };
    case "set_webhook_logs":
      return { ...state, webhookLogs: action.payload };
    default:
      return state;
  }
}

const AppStateContext = createContext<AppState | undefined>(undefined);
const AppDispatchContext = createContext<React.Dispatch<Action> | undefined>(undefined);

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(reducer, initialState);
  return (
    <AppStateContext.Provider value={state}>
      <AppDispatchContext.Provider value={dispatch}>{children}</AppDispatchContext.Provider>
    </AppStateContext.Provider>
  );
}

export function useAppState() {
  const context = useContext(AppStateContext);
  if (!context) {
    throw new Error("useAppState must be used within AppProvider");
  }
  return context;
}

export function useAppDispatch() {
  const context = useContext(AppDispatchContext);
  if (!context) {
    throw new Error("useAppDispatch must be used within AppProvider");
  }
  return context;
}
