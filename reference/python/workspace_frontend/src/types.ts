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

export type AttentionKind =
  | "waiting-approval"
  | "waiting-input"
  | "reconciliation-required"
  | "guarded-action-failed"
  | "recoverable-system-condition"
  | "recent-outcome"
  | "informational";

export type AttentionGroup =
  | "decision-required"
  | "blocked-failed"
  | "reconciliation-required"
  | "recent-outcome"
  | "informational";

export type AttentionUrgency = "high" | "medium" | "low";
export type ProjectionFreshness = "fresh" | "stale" | "degraded";

export type AttentionItem = {
  id: string;
  kind: AttentionKind;
  group: AttentionGroup;
  urgency: AttentionUrgency;
  title: string;
  reason: string;
  source: string;
  next_step: string;
  evidence_mode: "live" | "scenario";
  observed_at: string | null;
  open_href: string;
  interaction: "inspect-only";
  technical_evidence_available: boolean;
  authority_provided: false;
};

export type MyWorkProjection = {
  schema: "arvectum.workspace.my-work/1";
  generated_at: string;
  projection: {
    derived: true;
    canonical_authority: false;
    organizational_authority_provided: false;
    consequential_action_available: false;
    visibility_implies_permission: false;
  };
  scope: {
    organization_resolved_server_side: true;
    actor_resolved_server_side: true;
    denied_item_counts_exposed: false;
  };
  health: {
    state: ProjectionFreshness;
    code: string;
    message: string;
    observed_at: string;
    heartbeat_age_seconds: number | null;
  };
  items: AttentionItem[];
};
