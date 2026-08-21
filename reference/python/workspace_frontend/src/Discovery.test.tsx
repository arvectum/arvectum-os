import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { Discovery } from "./Discovery";
import { ObjectDetail } from "./ObjectDetail";
import type { DiscoveryProjection, ObjectContext } from "./types";

const projection: DiscoveryProjection = {
  schema: "arvectum.workspace.discovery/1",
  generated_at: "2026-08-21T12:00:00Z",
  query: "0344100006426000005",
  kind_filter: null,
  projection: {
    derived: true,
    canonical_authority: false,
    organizational_authority_provided: false,
    consequential_action_available: false,
    search_result_is_authority: false,
  },
  scope: {
    organization_resolved_server_side: true,
    actor_resolved_server_side: true,
    denied_result_counts_exposed: false,
    protected_snippets_minimized: true,
  },
  health: {
    state: "fresh",
    code: "OK",
    message: "Search was rebuilt from the current authorized governed source snapshot.",
    observed_at: "2026-08-21T12:00:00Z",
  },
  results: [{
    id: "0123456789abcdef0123",
    kind: "document",
    semantic_role: "Document",
    title: "Document — EIS exact notice attachment evidence",
    summary: "Governed Document available from ЕИС / zakupki.gov.ru.",
    source: "ЕИС / zakupki.gov.ru",
    authority_mode: "External Reference",
    state: "admitted · CAP-004 reconstruction complete",
    knowledge_role: null,
    open_href: "/objects/0123456789abcdef0123",
    interaction: "inspect-only",
    authority_provided: false,
  }],
};

const objectContext: ObjectContext = {
  schema: "arvectum.workspace.object-context/1",
  id: "0123456789abcdef0123",
  kind: "document",
  semantic_role: "Document",
  title: "Document — EIS exact notice attachment evidence",
  summary: "Governed Document available from ЕИС / zakupki.gov.ru.",
  source: "ЕИС / zakupki.gov.ru",
  knowledge_role: null,
  authority: {
    mode: "External Reference",
    scope: "EIS exact notice attachment evidence",
    authoritative_source: "ЕИС / zakupki.gov.ru",
    organizational_authority_provided: false,
    visibility_implies_permission: false,
  },
  state: {
    lifecycle: "admitted",
    validation: "CAP-004 reconstruction complete",
    classification: "internal",
  },
  context: {
    meaning: "Governed Document available from ЕИС / zakupki.gov.ru.",
    process: "This object is connected to retained governed execution/provenance evidence.",
    next_step: "Inspect the waiting governance gates before any consequential action.",
    interaction: "inspect-only",
    consequential_action_available: false,
  },
  technical: {
    subject_identity: "document-subject/internal-exact",
    version_identity: "document-version/internal-exact-v1",
    schema_version: "1",
    source_release_sha: "release-sha",
    provenance_refs: ["event-version/admitted-v1"],
    related_execution_subject: "execution-subject/exact",
    related_execution_version: "execution-version/exact-v5",
    related_event_version: "event-version/admitted-v1",
    related_checkpoint: "checkpoint-exact",
  },
  governed_preflight: {
    outcome: "Waiting",
    waiting_gates: ["Authorization", "Organizational Authority", "Data Governance", "Consequential Approval"],
    authority_provided: false,
  },
  projection: {
    presentation_authority: "non-authoritative",
    current_source_revalidated: true,
    exact_version_exposed_on_demand: true,
  },
};

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  window.history.replaceState({}, "", "/");
});

describe("P9.05 discovery", () => {
  it("finds the real-document shape by human notice context without rendering internal ids", async () => {
    window.history.replaceState({}, "", "/search?q=0344100006426000005");
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(projection), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    })));
    render(<Discovery />);
    expect(await screen.findByRole("heading", { name: "Document — EIS exact notice attachment evidence" })).toBeTruthy();
    expect(screen.getByText("ЕИС / zakupki.gov.ru")).toBeTruthy();
    expect(screen.getByText(/Derived search · never canonical authority/)).toBeTruthy();
    expect(screen.queryByText("document-subject/internal-exact")).toBeNull();
    expect(screen.getByRole("link", { name: "Open context" })).toBeTruthy();
  });

  it("preserves Knowledge semantic distinctions", async () => {
    const knowledge: DiscoveryProjection = {
      ...projection,
      query: "",
      kind_filter: "knowledge",
      results: [{
        ...projection.results[0],
        id: "11111111111111111111",
        kind: "knowledge",
        semantic_role: "Observation",
        title: "Observation — Arvectum OS governed state",
        summary: "Observation — not validated Knowledge. Governed Observation available from Arvectum OS governed state.",
        source: "Arvectum OS governed state",
        authority_mode: "Native",
        knowledge_role: "Observation — not validated Knowledge",
        open_href: "/objects/11111111111111111111",
      }],
    };
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(knowledge), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    })));
    render(<Discovery kind="knowledge" />);
    expect(await screen.findByText("Observation — not validated Knowledge")).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Observation — Arvectum OS governed state" })).toBeTruthy();
  });

  it("keeps denied or unavailable results minimized", async () => {
    const degraded: DiscoveryProjection = {
      ...projection,
      query: "secret",
      results: [],
      health: {
        state: "degraded",
        code: "DISCOVERY_SOURCE_UNAVAILABLE",
        message: "Current protected discovery sources could not be revalidated. Results are withheld.",
        observed_at: "2026-08-21T12:00:00Z",
      },
    };
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(degraded), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    })));
    render(<Discovery />);
    expect(await screen.findByRole("heading", { name: "Results withheld" })).toBeTruthy();
    expect(screen.queryByText(/secret object/i)).toBeNull();
  });

  it("opens human context first and keeps exact ids in technical drill-down", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(objectContext), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    })));
    render(<ObjectDetail objectId="0123456789abcdef0123" />);
    expect(await screen.findByRole("heading", { name: "Document — EIS exact notice attachment evidence" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "What this is" })).toBeTruthy();
    expect(screen.getByText("External Reference")).toBeTruthy();
    expect(screen.getByText(/This read-only view grants no Authorization/)).toBeTruthy();
    expect(screen.getByText("Outcome: Waiting.")).toBeTruthy();
    const technical = screen.getByText("Exact technical identity and provenance");
    fireEvent.click(technical);
    expect(screen.getByText("document-subject/internal-exact")).toBeTruthy();
    expect(screen.getByText("document-version/internal-exact-v1")).toBeTruthy();
    expect(screen.getByText("execution-version/exact-v5")).toBeTruthy();
  });
});
