/** Typed API client for MemoMeet backend — see docs/API_STRUCTURE.md */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function apiFetch<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });
  const json = await res.json();
  if (!json.success) throw new Error(json.error?.message || "API error");
  return json.data;
}

// TODO: Add typed methods — customers, meetings, truth, assistant, etc.
