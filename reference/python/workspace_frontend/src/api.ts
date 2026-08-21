import type { WorkspaceContext } from "./types";

export class WorkspaceApiError extends Error {
  readonly code: string;
  readonly reloadRequired: boolean;

  constructor(code: string, reloadRequired = false) {
    super(code);
    this.name = "WorkspaceApiError";
    this.code = code;
    this.reloadRequired = reloadRequired;
  }
}

const RELEASE_ID = __ARVECTUM_WORKSPACE_RELEASE__;

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set("X-Arvectum-Workspace-Release", RELEASE_ID);
  if (init.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  const response = await fetch(path, { ...init, headers, credentials: "same-origin" });
  if (!response.ok) {
    let payload: { code?: string; detail?: string; reload_required?: boolean } = {};
    try {
      payload = await response.json();
    } catch {
      // Keep a minimized browser error when the response is not JSON.
    }
    throw new WorkspaceApiError(
      payload.code ?? payload.detail ?? `HTTP_${response.status}`,
      Boolean(payload.reload_required),
    );
  }
  return (await response.json()) as T;
}

export async function loadWorkspaceContext(): Promise<WorkspaceContext> {
  try {
    return await request<WorkspaceContext>("/api/app/v1/context");
  } catch (error) {
    if (error instanceof WorkspaceApiError && error.code === "SESSION_REQUIRED") {
      return request<WorkspaceContext>("/api/app/v1/session/bootstrap", { method: "POST" });
    }
    throw error;
  }
}

export async function logoutWorkspace(csrfToken: string): Promise<void> {
  await request<{ status: string }>("/api/app/v1/session/logout", {
    method: "POST",
    headers: { "X-Arvectum-CSRF": csrfToken },
  });
}

export const workspaceReleaseId = RELEASE_ID;
