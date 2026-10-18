// One place for all backend calls: base URL, bearer token,
// one automatic token refresh on 401, and typed errors.
import { tokens } from "./tokens";

const BASE: string = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export class HttpError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}
export class NetworkError extends Error {}

async function send(path: string, options: RequestInit): Promise<Response> {
  const headers = new Headers(options.headers);
  if (options.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  if (tokens.access) headers.set("Authorization", `Bearer ${tokens.access}`);
  try {
    return await fetch(`${BASE}${path}`, { ...options, headers });
  } catch (e) {
    if (e instanceof DOMException && e.name === "AbortError") throw e;
    throw new NetworkError("Can't reach the server. Check your connection.");
  }
}

let refreshing: Promise<boolean> | null = null;

async function refresh(): Promise<boolean> {
  if (!tokens.refresh) return false;
  refreshing ??= (async () => {
    try {
      const res = await fetch(`${BASE}/auth/refresh`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: tokens.refresh }),
      });
      if (!res.ok) { tokens.clear(); return false; }
      const data = await res.json();
      tokens.set(data.access_token, data.refresh_token ?? tokens.refresh);
      return true;
    } catch {
      return false;
    } finally {
      refreshing = null;
    }
  })();
  return refreshing;
}

// RFC 7807 uses `detail`/`title`; FastAPI validation errors use a `detail` array.
function messageFrom(body: any, fallback: string): string {
  const d = body?.detail ?? body?.title;
  if (typeof d === "string") return d;
  if (Array.isArray(d)) return d.map((x) => x?.msg ?? String(x)).join("; ");
  return fallback || "Something went wrong.";
}

export async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  let res = await send(path, options);
  if (res.status === 401 && !path.startsWith("/auth/") && (await refresh())) {
    res = await send(path, options);
  }
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new HttpError(res.status, messageFrom(body, res.statusText));
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}
