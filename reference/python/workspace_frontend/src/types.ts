export type NavigationItem = {
  id: string;
  label: string;
  href: string;
  availability: "available" | `planned-${string}`;
};

export type WorkspaceContext = {
  schema: "arvectum.workspace.shell-context/1";
  release: {
    id: string;
    app_api_contract: string;
    classification: "bounded-internal-provisional";
    public_api: false;
  };
  organization: {
    label: string;
    scope_resolved_server_side: true;
  };
  actor: {
    label: string;
    attributable: true;
    scope_resolved_server_side: true;
    authentication_source: string;
  };
  session: {
    csrf_token: string;
    bounded: true;
    revocable: true;
    authority_provided: false;
  };
  navigation: NavigationItem[];
  data_governance: {
    protected_read_revalidated: true;
    response_minimized: "shell-context-only";
    canonical_state_in_browser: false;
  };
};
