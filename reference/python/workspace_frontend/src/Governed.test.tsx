import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { Governed } from "./Governed";
import type { GovernedExperienceProjection, GovernedPreflightResult } from "./types";

const projection: GovernedExperienceProjection = {
  schema: "arvectum.workspace.governed-experience/1",
  generated_at: "2026-08-21T12:00:00Z",
  presentation: {
    title: "EIS document governed execution",
    summary: "A real retained execution/provenance chain for an EIS-backed governed document.",
    source: "ЕИС / zakupki.gov.ru",
    authority_mode: "External Reference",
    authority_scope: "EIS exact notice attachment evidence",
    validation_status: "CAP-004 reconstruction complete",
  },
  execution: {
    status: "Waiting",
    meaning: "Required action decisions are still unresolved, so the execution remains fail-closed.",
    waiting_decisions: ["Authorization", "Organizational Authority", "Data Governance", "Consequential Approval"],
    technical_identity_available: true,
  },
  decisions: [
    { name: "Authorization", state: "Waiting", basis: "No action-specific authorization decision supplied." },
    { name: "Organizational Authority", state: "Waiting", basis: "Technical access supplies no Organizational Authority." },
    { name: "Data Governance", state: "Waiting", basis: "No purpose-specific data-governance decision supplied." },
    { name: "Consequential Approval", state: "Waiting", basis: "The browser/session/button is not approval." },
  ],
  action: {
    kind: "governed-preflight",
    label: "Run governed preflight",
    available: true,
    consequential: false,
    canonical_mutation_requested: false,
    external_effect_requested: false,
    authority_provided: false,
    explanation: "Re-check the real retained execution and all four governance gates now.",
  },
  technical: {
    release_sha: "a".repeat(40),
    source_subject: "document-subject/eis-real",
    source_version: "document-version/eis-real-v1",
    execution_subject: "execution-subject/eis-real",
    execution_version: "execution-version/eis-real-v5",
    event_version: "event-version/eis-real-v1",
    checkpoint_id: "checkpoint-real",
    provenance_refs: ["event-version/eis-real-v1"],
  },
  scope: {
    organization_resolved_server_side: true,
    actor_resolved_server_side: true,
    current_access_revalidated: true,
    organizational_authority_provided: false,
    visibility_implies_permission: false,
  },
};

const result: GovernedPreflightResult = {
  schema: "arvectum.workspace.governed-preflight-result/1",
  recorded_at: "2026-08-21T12:01:00Z",
  outcome: "Waiting",
  status_text: "Preflight executed: WAITING / fail-closed. Missing governance decisions were not manufactured.",
  canonical_mutation_requested: false,
  canonical_mutation_performed: false,
  external_effect_requested: false,
  external_effect_performed: false,
  organizational_authority_provided: false,
  consequential_approval_provided: false,
  evidence: {
    classification: "owner-local non-canonical proof evidence",
    sha256: "b".repeat(64),
  },
};

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe("P9.06 governed actions", () => {
  it("shows human execution context and all four independent decisions without requiring ids", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(projection), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    })));
    render(<Governed csrfToken="csrf-test" />);
    expect(await screen.findByRole("heading", { name: "EIS document governed execution" })).toBeTruthy();
    expect(screen.getByText("ЕИС / zakupki.gov.ru")).toBeTruthy();
    expect(screen.getByText("External Reference")).toBeTruthy();
    expect(screen.getAllByText("Waiting")).toHaveLength(5);
    expect(screen.getByText(/action button do not grant Authorization/)).toBeTruthy();
    expect(screen.getByRole("button", { name: "Run governed preflight" })).toBeTruthy();
  });

  it("runs bounded preflight with CSRF and reports fail-closed noncanonical evidence", async () => {
    const fetchMock = vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === "POST") {
        return new Response(JSON.stringify(result), { status: 200, headers: { "Content-Type": "application/json" } });
      }
      return new Response(JSON.stringify(projection), { status: 200, headers: { "Content-Type": "application/json" } });
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<Governed csrfToken="csrf-exact" />);
    fireEvent.click(await screen.findByRole("button", { name: "Run governed preflight" }));
    expect(await screen.findByText(/Preflight executed: WAITING \/ fail-closed/)).toBeTruthy();
    expect(screen.getByText(/owner-local non-canonical proof evidence/)).toBeTruthy();
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const [, postInit] = fetchMock.mock.calls[1];
    const headers = new Headers(postInit?.headers);
    expect(postInit?.method).toBe("POST");
    expect(headers.get("X-Arvectum-CSRF")).toBe("csrf-exact");
    expect(postInit?.body).toBeUndefined();
  });

  it("withholds protected execution detail when current source cannot be revalidated", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({ detail: "GOVERNED_EXPERIENCE_UNAVAILABLE" }), {
      status: 503,
      headers: { "Content-Type": "application/json" },
    })));
    render(<Governed csrfToken="csrf-test" />);
    expect(await screen.findByRole("heading", { name: "Current governed evidence is unavailable." })).toBeTruthy();
    expect(screen.queryByText("execution-version/eis-real-v5")).toBeNull();
  });
});
