export type DogfoodingJourney = "J1" | "J2" | "J3" | "J4" | "J5" | "J6" | "other";
export type DogfoodingSurface =
  | "home"
  | "organization"
  | "my-work"
  | "activity"
  | "search"
  | "records-documents-knowledge"
  | "ask-arvectum"
  | "governed-actions"
  | "products"
  | "other";
export type DogfoodingSeverity = "blocker" | "material" | "minor";
export type DogfoodingClassification = "workspace-usability" | "product-specific" | "governance" | "security-authority";
export type DogfoodingDisposition = "resolved" | "routed-product" | "routed-governance" | "not-reproducible" | "deferred";

export type DogfoodingObservationInput = {
  journey: DogfoodingJourney;
  surface: DogfoodingSurface;
  severity: DogfoodingSeverity;
  classification: DogfoodingClassification;
  summary: string;
  details: string;
};

export type DogfoodingObservation = DogfoodingObservationInput & {
  schema: "arvectum.workspace.dogfooding-observation/1";
  id: string;
  recorded_at: string;
  release_id: string;
  status: "open" | "dispositioned";
  disposition: DogfoodingDisposition | null;
  disposition_rationale: string | null;
  dispositioned_at: string | null;
};

export type DogfoodingBacklog = {
  schema: "arvectum.workspace.dogfooding-backlog/1";
  generated_at: string;
  projection: {
    derived: true;
    canonical_authority: false;
    canonical_event: false;
    validated_knowledge: false;
    organizational_authority_provided: false;
    consequential_action_available: false;
  };
  scope: {
    organization_resolved_server_side: true;
    actor_resolved_server_side: true;
    current_access_revalidated: true;
    cross_organization_aggregation: false;
  };
  retention: {
    bounded: true;
    days: number;
    max_items: number;
    free_text_minimized: true;
  };
  summary: {
    total: number;
    open: number;
    material_open: number;
  };
  items: DogfoodingObservation[];
};
