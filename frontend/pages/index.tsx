import { useEffect, useState } from "react";

const API = "http://localhost:8000";

type Task = { id: number; title: string; description: string; done: boolean };

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchTasks = async () => {
    const res = await fetch(`${API}/tasks`);
    setTasks(await res.json());
  };

  useEffect(() => { fetchTasks(); }, []);

  const addTask = async () => {
    if (!title.trim()) return;
    await fetch(`${API}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, description: desc }),
    });
    setTitle(""); setDesc("");
    fetchTasks();
  };

  const markDone = async (id: number) => {
    await fetch(`${API}/tasks/${id}/done`, { method: "PATCH" });
    fetchTasks();
  };

  const deleteTask = async (id: number) => {
    await fetch(`${API}/tasks/${id}`, { method: "DELETE" });
    fetchTasks();
  };

  const getSummary = async () => {
    setLoading(true);
    const res = await fetch(`${API}/summary`);
    const data = await res.json();
    setSummary(data.summary);
    setLoading(false);
  };

  return (
    <main style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>AI Task Manager</h1>

      {/* Add Task */}
      <div style={{ marginBottom: 20 }}>
        <input placeholder="Task title" value={title} onChange={e => setTitle(e.target.value)}
          style={{ width: "100%", padding: 8, marginBottom: 6 }} />
        <input placeholder="Description" value={desc} onChange={e => setDesc(e.target.value)}
          style={{ width: "100%", padding: 8, marginBottom: 6 }} />
        <button onClick={addTask} style={{ padding: "8px 16px", background: "#0070f3", color: "#fff", border: "none", cursor: "pointer" }}>
          Add Task
        </button>
      </div>

      {/* Task List */}
      {tasks.map(t => (
        <div key={t.id} style={{ border: "1px solid #ddd", padding: 12, marginBottom: 8, borderRadius: 6,
          opacity: t.done ? 0.5 : 1 }}>
          <strong style={{ textDecoration: t.done ? "line-through" : "none" }}>{t.title}</strong>
          <p style={{ margin: "4px 0", color: "#555" }}>{t.description}</p>
          <div style={{ display: "flex", gap: 8 }}>
            {!t.done && <button onClick={() => markDone(t.id)}>✅ Done</button>}
            <button onClick={() => deleteTask(t.id)} style={{ color: "red" }}>🗑 Delete</button>
          </div>
        </div>
      ))}

      {/* AI Summary */}
      <div style={{ marginTop: 24 }}>
        <button onClick={getSummary} style={{ padding: "8px 16px", background: "#6f42c1", color: "#fff", border: "none", cursor: "pointer" }}>
          {loading ? "Loading..." : "✨ Get AI Summary"}
        </button>
        {summary && <p style={{ marginTop: 12, background: "#f4f4f4", padding: 12, borderRadius: 6 }}>{summary}</p>}
      </div>
    </main>
  );
}
