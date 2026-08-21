import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { Products } from "./Products";
import type { ProductSurfacesProjection } from "./types";

const projection: ProductSurfacesProjection = {
  schema: "arvectum.workspace.product-surfaces/1",
  generated_at: "2026-08-21T14:00:00Z",
  projection: {
    derived: true,
    canonical_authority: false,
    product_business_logic_in_platform: false,
    hidden_coupling: false,
    consequential_action_available: false,
    visibility_implies_permission: false,
  },
  scope: {
    organization_resolved_server_side: true,
    actor_resolved_server_side: true,
    current_access_revalidated: true,
    cross_organization_composition: false,
  },
  products: [
    {
      id: "tender-operator",
      name: "Tender Operator",
      purpose: "44-ФЗ pre-bid review",
      evidence_state: "available",
      evidence_code: "PASS_RETAINED_P7_07_RELIANCE",
      source: "ЕИС / zakupki.gov.ru",
      authority_mode: "External Reference",
      summary: "Real retained tender evidence.",
      work: [
        { label: "Tender notice", value: "0344100006426000005", meaning: "Human case entry." },
        { label: "Current product work", value: "Pre-bid review", meaning: "Tender semantics remain product-owned." },
      ],
      boundary: {
        contract: "P6.02 — Tender Operator",
        governance_ref: "docs/contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md",
        version: "0.1.0",
        lifecycle: "Provisional",
        compatibility_line: "restricted-paid-pilot/44fz-prebid-v1",
        dependencies: ["CAP-001", "CAP-004"],
        explicitly_omitted_dependencies: ["CAP-002", "CAP-003"],
        product_semantics_owner: "product",
        platform_business_logic_owner: false,
        inspectable: true,
      },
      technical: {
        operational_contour: "P7.07",
        evidence_classification: "governed retained evidence",
        raw_product_state_exposed: false,
        raw_platform_identifiers_exposed: false,
      },
    },
    {
      id: "discount-parser",
      name: "Discount Parser",
      purpose: "Controlled Telegram publication reconstruction",
      evidence_state: "available",
      evidence_code: "PASS_RETAINED_P7_08_RECONSTRUCTION",
      source: "Discount Parser product evidence + Telegram external confirmation",
      authority_mode: "Derived reconstruction / External Reference",
      summary: "Real retained publication reconstruction.",
      work: [
        { label: "Offer", value: "offer-42", meaning: "Offer remains product-owned." },
        { label: "Publication", value: "publication-7", meaning: "Publication remains product-owned." },
      ],
      boundary: {
        contract: "P6.06 — Discount Parser",
        governance_ref: "docs/contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md",
        version: "0.1.0",
        lifecycle: "Provisional",
        compatibility_line: "mvp-v1/controlled-telegram-publication",
        dependencies: ["CAP-004"],
        explicitly_omitted_dependencies: ["CAP-001", "CAP-002", "CAP-003"],
        product_semantics_owner: "product",
        platform_business_logic_owner: false,
        inspectable: true,
      },
      technical: {
        operational_contour: "P7.08",
        evidence_classification: "non-canonical operational evidence",
        raw_product_state_exposed: false,
        raw_platform_identifiers_exposed: false,
      },
    },
  ],
};

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe("P9.07 product-owned surfaces", () => {
  it("shows two distinct real product contexts and inspectable provisional boundaries", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(projection), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    })));
    render(<Products />);

    expect(await screen.findByRole("heading", { name: "Tender Operator" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Discount Parser" })).toBeTruthy();
    expect(screen.getByText("0344100006426000005")).toBeTruthy();
    expect(screen.getByText("offer-42")).toBeTruthy();
    expect(screen.getByText("publication-7")).toBeTruthy();
    expect(screen.getAllByText("Product Contract boundary")).toHaveLength(2);
    expect(screen.getAllByText(/Provisional/)).toHaveLength(2);
    expect(screen.getByText(/without merging their domains/i)).toBeTruthy();
    expect(screen.queryByText(/approve/i)).toBeNull();
    expect(screen.queryByText(/publish now/i)).toBeNull();
  });

  it("withholds product work when retained evidence is unavailable", async () => {
    const unavailable: ProductSurfacesProjection = {
      ...projection,
      products: [{
        ...projection.products[1],
        evidence_state: "unavailable",
        evidence_code: "DISCOUNT_REVALIDATION_UNAVAILABLE",
        work: [],
        summary: "Current retained Discount Parser reconstruction could not be revalidated; no product data is shown.",
      }],
    };
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(unavailable), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    })));
    render(<Products />);
    expect(await screen.findByRole("heading", { name: "Discount Parser" })).toBeTruthy();
    expect(screen.getByText(/Product-specific work is withheld/)).toBeTruthy();
    expect(screen.queryByText("offer-42")).toBeNull();
  });
});
