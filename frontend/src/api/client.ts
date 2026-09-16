const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
  ?? `http://${window.location.hostname || "127.0.0.1"}:8000/api/v1`;
export const AUTH_REQUIRED_EVENT = "skillway:auth-required";
export const API_DOCS_URL = API_BASE_URL.replace(/\/api\/v1\/?$/, "/docs");

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!response.ok) {
    if (response.status === 401) window.dispatchEvent(new Event(AUTH_REQUIRED_EVENT));
    const body = await response.json().catch(() => null);
    const message = body?.detail ?? `API request failed: ${response.status}`;
    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

export async function apiGet<T>(path: string): Promise<T> {
  return request<T>(path);
}

export async function apiPost<T>(path: string, body?: unknown): Promise<T> {
  return request<T>(path, {
    method: "POST",
    body: body === undefined ? undefined : JSON.stringify(body),
  });
}
