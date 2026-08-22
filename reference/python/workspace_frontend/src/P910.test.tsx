import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { Organization } from "./Organization";
import type { OrganizationCompositionProjection } from "./types";

const composition: OrganizationCompositionProjection = {
  schema: "arvectum.workspace.organization-composition/1",
  generated_at: "2026-08-22T07:00:00Z",
  health: { state: "ready" },
  projection: {
    derived: true, canonical_authority: false, organizational_authority_provided: false,
    company_semantics_promoted_to_kernel: false, project_lenses_are_canonical_records: false,
    source_projection_authority_preserved: true, canonical_mutation_available: false, external_effect_available: false,
  },
  scope: {
    organization_resolved_server_side: true, actor_resolved_server_side: true, current_access_revalidated: true,
    cross_organization_aggregation: false, denied_source_counts_exposed: false,
  },
  lanes: [
    { id: "products", label: "Products", summary: "Explicit product boundaries.", state: "ready", source_boundary: "P9.07 product-owned composition", items: [
      { id: "product:tender", kind: "product", label: "Tender Operator", summary: "Product context", href: "/products/tender-operator", source: "P7.07", authority: "ЕИС — External Reference", ownership: "product-owned", state: "verified", provenance_available: true, canonical_project_record: false, interaction: "navigate-and-inspect", authority_provided: false, consequential_action_available: false },
    ] },
    { id: "projects", label: "Project lenses", summary: "Navigation lenses.", state: "ready", source_boundary: "Declared product contours", items: [
      { id: "project-lens:tender", kind: "project-lens", label: "Tender Operator operating contour", summary: "Not a canonical Project record.", href: "/products/tender-operator", source: "P7.07", authority: "ЕИС — External Reference", ownership: "product-owned source; Workspace navigation lens", state: "verified", provenance_available: true, canonical_project_record: false, interaction: "navigate-and-inspect", authority_provided: false, consequential_action_available: false },
    ] },
    { id: "knowledge", label: "Knowledge", summary: "Governed context.", state: "ready", source_boundary: "P9.05 Discovery", items: [] },
    { id: "work", label: "Work", summary: "Attention context.", state: "ready", source_boundary: "P9.04/P9.09 attention", items: [] },
  ],
};

afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe("P9.10 organization composition", () => {
  it("presents company-level navigation while keeping project lenses explicitly non-canonical", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(composition), { status: 200, headers: { "Content-Type": "application/json" } })));
    render(<Organization organizationLabel={'ООО «Арвектум»'} />);
    expect(await screen.findByRole("heading", { name: 'ООО «Арвектум»' })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Products" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Project lenses" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Knowledge" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Work" })).toBeTruthy();
    expect(screen.getAllByText(/not a canonical Project record/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/does not create Organizational Authority/)).toBeTruthy();
    expect(screen.getAllByRole("link", { name: "Open context" }).map((link) => link.getAttribute("href"))).toContain("/products/tender-operator");
  });

  it("does not retain company context when the protected composition endpoint is denied", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({ detail: "ACCESS_DENIED" }), { status: 403, headers: { "Content-Type": "application/json" } })));
    render(<Organization organizationLabel={'ООО «Арвектум»'} />);
    expect(await screen.findByRole("heading", { name: "Organization context is unavailable." })).toBeTruthy();
    expect(screen.queryByText("Tender Operator")).toBeNull();
  });
});
