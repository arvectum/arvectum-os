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

export type DiscoveryKind = "record" | "document" | "knowledge" | "execution";
export type DiscoveryFreshness = "fresh" | "degraded";

export type DiscoveryResult = {
  id: string;
  kind: DiscoveryKind;
  semantic_role: string;
  title: string;
  summary: string;
  source: string;
  authority_mode: string;
  state: string;
  knowledge_role: string | null;
  open_href: string;
  interaction: "inspect-only";
  authority_provided: false;
};

export type DiscoveryProjection = {
  schema: "arvectum.workspace.discovery/1";
  generated_at: string;
  query: string;
  kind_filter: DiscoveryKind | null;
  projection: {
    derived: true;
    canonical_authority: false;
    organizational_authority_provided: false;
    consequential_action_available: false;
    search_result_is_authority: false;
  };
  scope: {
    organization_resolved_server_side: true;
    actor_resolved_server_side: true;
    denied_result_counts_exposed: false;
    protected_snippets_minimized: true;
  };
  health: {
    state: DiscoveryFreshness;
    code: string;
    message: string;
    observed_at: string;
  };
  results: DiscoveryResult[];
};

export type ObjectContext = {
  schema: "arvectum.workspace.object-context/1";
  id: string;
  kind: DiscoveryKind;
  semantic_role: string;
  title: string;
  summary: string;
  source: string;
  knowledge_role: string | null;
  authority: {
    mode: string;
    scope: string;
    authoritative_source: string;
    organizational_authority_provided: false;
    visibility_implies_permission: false;
  };
  state: {
    lifecycle: string | null;
    validation: string | null;
    classification: string;
  };
  context: {
    meaning: string;
    process: string;
    next_step: string;
    interaction: "inspect-only";
    consequential_action_available: false;
  };
  technical: {
    subject_identity: string;
    version_identity: string;
    schema_version: string;
    source_release_sha: string;
    provenance_refs: string[];
    related_execution_subject: string | null;
    related_execution_version: string | null;
    related_event_version: string | null;
    related_checkpoint: string | null;
  };
  governed_preflight: {
    outcome: string | null;
    waiting_gates: string[];
    authority_provided: false;
  } | null;
  projection: {
    presentation_authority: "non-authoritative";
    current_source_revalidated: true;
    exact_version_exposed_on_demand: true;
  };
};
