import type { CreditsBalance, CreditUsageItem, Task, User } from "./types";

const API_BASE_URL =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? "http://127.0.0.1:8000";
const MOCK = (import.meta.env.VITE_MOCK_API as string | undefined) === "1";

function authHeaders(token: string | null): HeadersInit {
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function http<T>(path: string, init: RequestInit & { token?: string | null } = {}): Promise<T> {
  if (!API_BASE_URL) {
    throw new Error("VITE_API_BASE_URL is not set (or enable VITE_MOCK_API=1)");
  }

  const { token, ...rest } = init;
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...rest,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(token ?? null),
      ...(rest.headers ?? {})
    }
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Request failed: ${res.status}`);
  }

  // Many endpoints return JSON, but DELETE often returns 204 No Content.
  if (res.status === 204) {
    return undefined as T;
  }

  const contentType = res.headers.get("content-type") ?? "";
  if (!contentType.includes("application/json")) {
    return undefined as T;
  }

  return (await res.json()) as T;
}

export async function register(email: string, password: string): Promise<{ token: string; user: User }> {
  if (MOCK) {
    return {
      token: "mock-token",
      user: { id: 123, email }
    };
  }

  // fastapi_app contract: POST /auth/register -> { access_token, token_type }
  const tokenResp = await http<{ access_token: string }>("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password })
  });

  const user = await me(tokenResp.access_token);
  return { token: tokenResp.access_token, user };
}

export async function login(email: string, password: string): Promise<{ token: string; user: User }> {
  if (MOCK) {
    return {
      token: "mock-token",
      user: { id: 123, email }
    };
  }

  // fastapi_app contract: POST /auth/login -> { access_token, token_type }
  const tokenResp = await http<{ access_token: string }>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password })
  });

  const user = await me(tokenResp.access_token);
  return { token: tokenResp.access_token, user };
}

export async function me(token: string): Promise<User> {
  if (MOCK) {
    return { id: 123, email: "student@example.com" };
  }

  // fastapi_app contract: GET /auth/me
  return http("/auth/me", { method: "GET", token });
}

export async function getCreditsBalance(token: string): Promise<CreditsBalance> {
  if (MOCK) {
    const now = new Date();
    const resets = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() + 1, 1));
    return {
      plan: "student",
      monthly_allowance: 200,
      remaining: 187,
      resets_at_iso: resets.toISOString()
    };
  }

  // Backend contract (stub for now): GET /credits/balance
  return http("/credits/balance", { method: "GET", token });
}

export async function getCreditsUsage(token: string): Promise<CreditUsageItem[]> {
  if (MOCK) {
    const base = new Date();
    return [
      {
        id: "cu_1",
        at_iso: new Date(base.getTime() - 1000 * 60 * 60 * 2).toISOString(),
        action: "generate_app_spec",
        cost: 1
      },
      {
        id: "cu_2",
        at_iso: new Date(base.getTime() - 1000 * 60 * 25).toISOString(),
        action: "validate_code",
        cost: 1
      }
    ];
  }

  // Backend contract (stub for now): GET /credits/usage
  return http("/credits/usage", { method: "GET", token });
}

export async function listTasks(token: string): Promise<Task[]> {
  if (MOCK) {
    return [
      {
        id: 1,
        owner_id: 123,
        title: "Draft app spec",
        description: "Write the initial requirements and constraints",
        is_done: false
      },
      {
        id: 2,
        owner_id: 123,
        title: "Run backend tests",
        description: null,
        is_done: true
      }
    ];
  }

  return http("/tasks", { method: "GET", token });
}

export async function createTask(
  token: string,
  title: string,
  description: string | null
): Promise<Task> {
  if (MOCK) {
    return {
      id: Math.floor(Math.random() * 100000),
      owner_id: 123,
      title,
      description,
      is_done: false
    };
  }

  return http("/tasks", {
    method: "POST",
    token,
    body: JSON.stringify({ title, description })
  });
}

export async function updateTask(
  token: string,
  taskId: number,
  updates: Partial<Pick<Task, "title" | "description" | "is_done">>
): Promise<Task> {
  if (MOCK) {
    return {
      id: taskId,
      owner_id: 123,
      title: updates.title ?? "Mock task",
      description: updates.description ?? null,
      is_done: updates.is_done ?? false
    };
  }

  return http(`/tasks/${taskId}`, {
    method: "PATCH",
    token,
    body: JSON.stringify(updates)
  });
}

export async function deleteTask(token: string, taskId: number): Promise<void> {
  if (MOCK) {
    return;
  }

  await http<void>(`/tasks/${taskId}`, { method: "DELETE", token });
}
