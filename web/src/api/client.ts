const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export interface Health {
  status: string;
  environment: string;
  version: string;
}

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`${path} failed: ${response.status} ${response.statusText}`);
  }
  return (await response.json()) as T;
}

export function getHealth(): Promise<Health> {
  return request<Health>("/health");
}
