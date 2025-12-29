import React, { useEffect, useMemo, useState } from "react";

import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import * as api from "../services/api";
import type { Task } from "../services/types";
import { useAuth } from "../state/auth";

export default function TasksPage() {
  const { token } = useAuth();

  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [newTitle, setNewTitle] = useState("");
  const [newDescription, setNewDescription] = useState("");
  const [creating, setCreating] = useState(false);

  const [editingId, setEditingId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState("");
  const [editDescription, setEditDescription] = useState("");
  const [saving, setSaving] = useState(false);

  const sortedTasks = useMemo(() => {
    const copy = [...tasks];
    copy.sort((a, b) => {
      if (a.is_done !== b.is_done) return a.is_done ? 1 : -1;
      return b.id - a.id;
    });
    return copy;
  }, [tasks]);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      if (!token) return;
      setLoading(true);
      setError(null);
      try {
        const list = await api.listTasks(token);
        if (!cancelled) setTasks(list);
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : "Failed to load tasks");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    void load();
    return () => {
      cancelled = true;
    };
  }, [token]);

  function startEdit(t: Task) {
    setEditingId(t.id);
    setEditTitle(t.title);
    setEditDescription(t.description ?? "");
  }

  function cancelEdit() {
    setEditingId(null);
    setEditTitle("");
    setEditDescription("");
  }

  async function onCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!token) return;

    setCreating(true);
    setError(null);
    try {
      const created = await api.createTask(token, newTitle.trim(), newDescription.trim() || null);
      setTasks((prev) => [created, ...prev]);
      setNewTitle("");
      setNewDescription("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create task");
    } finally {
      setCreating(false);
    }
  }

  async function onSave(taskId: number) {
    if (!token) return;
    setSaving(true);
    setError(null);
    try {
      const updated = await api.updateTask(token, taskId, {
        title: editTitle.trim(),
        description: editDescription.trim() || null
      });
      setTasks((prev) => prev.map((t) => (t.id === taskId ? updated : t)));
      cancelEdit();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update task");
    } finally {
      setSaving(false);
    }
  }

  async function onToggleDone(t: Task) {
    if (!token) return;
    setError(null);
    const nextDone = !t.is_done;
    setTasks((prev) => prev.map((x) => (x.id === t.id ? { ...x, is_done: nextDone } : x)));
    try {
      const updated = await api.updateTask(token, t.id, { is_done: nextDone });
      setTasks((prev) => prev.map((x) => (x.id === t.id ? updated : x)));
    } catch (err) {
      setTasks((prev) => prev.map((x) => (x.id === t.id ? t : x)));
      setError(err instanceof Error ? err.message : "Failed to update task");
    }
  }

  async function onDelete(taskId: number) {
    if (!token) return;
    setError(null);
    const snapshot = tasks;
    setTasks((prev) => prev.filter((t) => t.id !== taskId));
    try {
      await api.deleteTask(token, taskId);
      if (editingId === taskId) cancelEdit();
    } catch (err) {
      setTasks(snapshot);
      setError(err instanceof Error ? err.message : "Failed to delete task");
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Tasks</h1>
        <p className="text-sm text-gray-600">Create tasks, mark them done, and keep track of work.</p>
      </div>

      {error ? <div className="text-sm text-red-600">{error}</div> : null}

      <Card>
        <CardHeader>
          <CardTitle>Create</CardTitle>
          <CardDescription>Add a new task</CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-4" onSubmit={onCreate}>
            <div className="space-y-2">
              <Label htmlFor="title">Title</Label>
              <Input
                id="title"
                value={newTitle}
                onChange={(e) => setNewTitle(e.target.value)}
                placeholder="e.g. Implement tasks UI"
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="desc">Description (optional)</Label>
              <Input
                id="desc"
                value={newDescription}
                onChange={(e) => setNewDescription(e.target.value)}
                placeholder="Short details"
              />
            </div>

            <Button type="submit" disabled={creating}>
              {creating ? "Creating..." : "Create task"}
            </Button>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>List</CardTitle>
          <CardDescription>Your tasks (done tasks are shown last)</CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="text-sm text-gray-600">Loading...</div>
          ) : sortedTasks.length ? (
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead>
                  <tr className="text-left text-gray-500">
                    <th className="py-2 pr-4">Title</th>
                    <th className="py-2 pr-4">Description</th>
                    <th className="py-2 pr-4">Status</th>
                    <th className="py-2 pr-4">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {sortedTasks.map((t) => {
                    const isEditing = editingId === t.id;
                    return (
                      <tr key={t.id} className="border-t align-top">
                        <td className="py-2 pr-4">
                          {isEditing ? (
                            <Input value={editTitle} onChange={(e) => setEditTitle(e.target.value)} />
                          ) : (
                            <div className={t.is_done ? "line-through text-gray-500" : "text-gray-900"}>
                              {t.title}
                            </div>
                          )}
                        </td>
                        <td className="py-2 pr-4">
                          {isEditing ? (
                            <Input
                              value={editDescription}
                              onChange={(e) => setEditDescription(e.target.value)}
                              placeholder="(optional)"
                            />
                          ) : (
                            <div className="text-gray-600">{t.description ?? "—"}</div>
                          )}
                        </td>
                        <td className="py-2 pr-4 whitespace-nowrap">
                          <div className={t.is_done ? "text-gray-600" : "text-gray-900"}>
                            {t.is_done ? "Done" : "Open"}
                          </div>
                        </td>
                        <td className="py-2 pr-4 whitespace-nowrap">
                          <div className="flex items-center gap-2">
                            {isEditing ? (
                              <>
                                <Button onClick={() => onSave(t.id)} disabled={saving}>
                                  {saving ? "Saving..." : "Save"}
                                </Button>
                                <Button variant="secondary" type="button" onClick={cancelEdit} disabled={saving}>
                                  Cancel
                                </Button>
                              </>
                            ) : (
                              <>
                                <Button variant="secondary" type="button" onClick={() => onToggleDone(t)}>
                                  {t.is_done ? "Mark open" : "Mark done"}
                                </Button>
                                <Button variant="ghost" type="button" onClick={() => startEdit(t)}>
                                  Edit
                                </Button>
                                <Button variant="ghost" type="button" onClick={() => onDelete(t.id)}>
                                  Delete
                                </Button>
                              </>
                            )}
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-sm text-gray-600">No tasks yet. Create your first one above.</div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
