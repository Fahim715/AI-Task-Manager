"use client";

import { DragDropContext, Droppable, Draggable, DropResult } from "@hello-pangea/dnd";
import type { Task, TaskStatus } from "../lib/types";

interface KanbanBoardProps {
  tasks: Task[];
  onMove: (id: number, status: TaskStatus) => void;
}

const columns: { key: TaskStatus; title: string }[] = [
  { key: "todo", title: "Todo" },
  { key: "in_progress", title: "In Progress" },
  { key: "done", title: "Done" },
];

export function KanbanBoard({ tasks, onMove }: KanbanBoardProps) {
  const grouped = columns.reduce<Record<string, Task[]>>((acc, col) => {
    acc[col.key] = tasks.filter((task) => task.status === col.key);
    return acc;
  }, {});

  const handleDragEnd = (result: DropResult) => {
    if (!result.destination) return;
    const status = result.destination.droppableId as TaskStatus;
    const taskId = Number(result.draggableId);
    onMove(taskId, status);
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <div className="grid gap-4 md:grid-cols-3">
        {columns.map((col) => (
          <Droppable droppableId={col.key} key={col.key}>
            {(provided) => (
              <div
                ref={provided.innerRef}
                {...provided.droppableProps}
                className="card p-4 min-h-[320px]"
              >
                <h3 className="text-sm font-semibold text-slate-600 uppercase tracking-[0.2em]">
                  {col.title}
                </h3>
                <div className="mt-4 space-y-3">
                  {grouped[col.key].map((task, index) => (
                    <Draggable draggableId={String(task.id)} index={index} key={task.id}>
                      {(dragProps) => (
                        <div
                          ref={dragProps.innerRef}
                          {...dragProps.draggableProps}
                          {...dragProps.dragHandleProps}
                          className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm"
                        >
                          <p className="font-semibold text-ink">{task.title}</p>
                          <p className="text-xs text-slate-500 mt-2">
                            {task.description || "No description"}
                          </p>
                        </div>
                      )}
                    </Draggable>
                  ))}
                </div>
                {provided.placeholder}
              </div>
            )}
          </Droppable>
        ))}
      </div>
    </DragDropContext>
  );
}
