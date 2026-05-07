"use client";

import { useEffect, useState } from "react";
import { KanbanBoard } from "../../../components/KanbanBoard";
import { api } from "../../../lib/api";
import type { Task, TaskStatus } from "../../../lib/types";

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [view, setView] = useState<"kanban" | "list">("kanban");
  const [statusFilter, setStatusFilter] = useState<"all" | TaskStatus>("all");
  const [title, setTitle] = useState("");

  const loadTasks = async () => {
    const data = await api.listTasks(statusFilter === "all" ? "" : `?status=${statusFilter}`);
    setTasks(data);
  };

  useEffect(() => {
    loadTasks().catch(() => setTasks([]));
  }, [statusFilter]);

  const handleCreate = async () => {
    if (!title.trim()) return;
    await api.createTask({ title });
    setTitle("");
    await loadTasks();
  };

  const handleMove = async (id: number, status: TaskStatus) => {
    await api.updateTask(id, { status });
    await loadTasks();
  };

  return (
    <section className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <h1 className="text-2xl font-display font-semibold">Tasks</h1>
        <div className="flex gap-2">
          <button
            className={`px-4 py-2 rounded-full ${view === "kanban" ? "bg-ink text-white" : "border"}`}
            onClick={() => setView("kanban")}
          >
            Kanban
          </button>
          <button
            className={`px-4 py-2 rounded-full ${view === "list" ? "bg-ink text-white" : "border"}`}
            onClick={() => setView("list")}
          >
            List
          </button>
        </div>
      </div>

      <div className="card p-4 flex flex-wrap items-center gap-3">
        <input
          className="flex-1 min-w-[220px] rounded-xl border border-slate-300 px-4 py-2"
          placeholder="New task title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <button className="px-4 py-2 rounded-xl bg-ink text-white" onClick={handleCreate}>
          Add task
        </button>
        <select
          className="rounded-xl border border-slate-300 px-3 py-2"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value as TaskStatus | "all")}
        >
          <option value="all">All</option>
          <option value="todo">Todo</option>
          <option value="in_progress">In progress</option>
          <option value="done">Done</option>
        </select>
      </div>

      {view === "kanban" ? (
        <KanbanBoard tasks={tasks} onMove={handleMove} />
      ) : (
        <div className="card p-4">
          <div className="grid gap-2">
            {tasks.map((task) => (
              <div key={task.id} className="border border-slate-200 rounded-xl p-4">
                <div className="flex items-center justify-between">
                  <p className="font-semibold">{task.title}</p>
                  <span className="text-xs uppercase text-slate-500">{task.status}</span>
                </div>
                <p className="text-sm text-slate-600 mt-2">{task.description || "No description"}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
