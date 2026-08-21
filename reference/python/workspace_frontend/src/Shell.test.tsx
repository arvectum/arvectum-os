import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Shell } from "./Shell";
import type { WorkspaceContext } from "./types";

const context: WorkspaceContext = {
  schema: "arvectum.workspace.shell-context/1",
  release: { id: "p9.03.1", app_api_contract: "1", classification: "bounded-internal-provisional", public_api: false },
  organization: { label: "ООО «Арвектум»", scope_resolved_server_side: true },
  actor: { label: "Owner operator", attributable: true, scope_resolved_server_side: true, authentication_source: "P7.04 owner-local credential" },
  session: { csrf_token: "test-only", bounded: true, revocable: true, authority_provided: false },
  navigation: [
    { id: "home", label: "Home", href: "/", availability: "available" },
    { id: "my-work", label: "My Work", href: "/my-work", availability: "planned-p9.04" }
  ],
  data_governance: { protected_read_revalidated: true, response_minimized: "shell-context-only", canonical_state_in_browser: false }
};

describe("P9.03 shell", () => {
  it("presents explicit Organization and attributable actor context", () => {
    window.history.replaceState({}, "", "/");
    render(<Shell context={context} onLogout={() => undefined} />);
    expect(screen.getByLabelText("Organization: ООО «Арвектум»")).toBeTruthy();
    expect(screen.getByLabelText("Authenticated actor: Owner operator")).toBeTruthy();
    expect(screen.getByRole("navigation", { name: "Workspace navigation" })).toBeTruthy();
    expect(screen.getByRole("link", { name: /My Work/ })).toBeTruthy();
    expect(screen.getByText("Not implied")).toBeTruthy();
  });
});
