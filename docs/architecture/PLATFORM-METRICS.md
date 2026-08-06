# Arvectum OS Platform Metrics

Status: `Informative`
Version: `0.4.0`
Updated: `2026-08-07`
Architecture basis: `RFC-0001 v0.7.0`
Constitution basis: `1.2.0`

## Purpose

This document defines the initial evidence framework for evaluating whether Arvectum OS creates measurable organizational and platform leverage.

Metrics, targets and cadence evolve with company stage, product portfolio and operating baseline. This document does not override the Constitution, accepted RFCs or product commitments.

## Measurement Principle

The platform is valuable only when it improves outcomes while preserving organizational control, security, portability and truthful conformance claims.

It must not be evaluated primarily by service count, abstraction count, RFC count, lines of code, infrastructure complexity or code nominally labeled as platform.

## Initial Metric Groups

### Product Delivery and Experimentation

- time from product need to bounded Product Experiment;
- time from validated experiment to usable incubating capability;
- platform-caused delivery delay;
- percentage of experiments with owner, review date and exit path;
- percentage promoted, contained or retired by the declared review date.

### Contract Proportionality

- percentage of completely product-local experiments conducted without unnecessary platform-contract work;
- time required to create a minimal Provisional Product Contract when platform interaction begins;
- experiments accessing platform capabilities or canonical state without a declared provisional contract;
- contract fields or controls found unnecessary for the actual interaction;
- product delay attributable to contract ceremony rather than risk control.

### Canonical Authority and External Systems

- percentage of Canonical Records with a declared authority mode;
- externally authoritative objects without a declared external-system reference;
- competing-source-of-truth incidents;
- Governed Replicas with overdue synchronization or unknown freshness;
- synchronization conflicts without a declared resolution rule;
- time to restore operation after an authoritative external system becomes unavailable.

### Scoped Conformance

- implementations claiming conformance with an up-to-date Conformance Statement;
- claims whose scope, lifecycle, data classes and applicable requirements are explicit;
- requirements marked not applicable without adequate rationale;
- manual or provisional controls without review or replacement conditions;
- overdue conformance reviews;
- known gaps without owner or remediation path;
- cases where limited conformance was presented as full-platform conformance.

### Reuse and Platform Gravity

- real consumers per capability;
- percentage of Active capabilities used by multiple consumers;
- time and cost to implement a second consumer;
- duplicated validated shared capabilities;
- capability adoption, bypass and abandonment;
- number and age of architectural exceptions.

### Economics

- capability responsibility and support cost;
- integration cost versus product-specific or external alternatives;
- measurable operating cost or risk avoided;
- de-platformization and retirement cost;
- cost of replacing a model or technology adapter.

### Governance and Explainability

- consequential executions with complete provenance;
- time required to reconstruct a consequential output;
- required approvals and validations captured correctly;
- unauthorized or unexplained canonical changes;
- change-failure rate for standards, policies and workflows.

### Security, Privacy and Isolation

- unauthorized access and tenant-isolation incidents;
- governed records with declared tenant scope and classification where required;
- actors and components reviewed for least privilege;
- sensitive-data operations with attributable audit records;
- overdue retention or deletion actions;
- data-minimization exceptions and their review age.

### Organizational Control and Portability

- time to produce a governed export within the declared conformance scope;
- export scope preserving identities, versions, authority modes, relationships and provenance;
- tested migration success rate;
- deletion requests completed under applicable policy;
- customer or organizational assets dependent on inaccessible proprietary representation;
- portability defects discovered during handover or migration tests.

### Capability Lifecycle

- duration of incubation;
- promotion rate to Active;
- return-to-product, replacement and retirement rate;
- overdue lifecycle reviews;
- Deprecated capabilities without migration plans;
- Active capabilities no longer satisfying admission criteria;
- exploratory areas incorrectly treated as funded roadmap commitments;
- Candidates incorrectly required to implement stable contracts before incubation.

### Reliability and Quality

- execution failure rate attributable to platform components;
- compatibility failures detected before execution;
- incidents caused by shared capabilities;
- recovery time from platform-caused failures;
- output-quality improvement attributable to shared validation or knowledge.

## Baselines and Targets

Targets require an operational baseline.

Every metric should identify definition, data source, owner, review period, baseline, target, rationale, limitations and possible harmful incentives.

A metric without a reliable data source is a hypothesis, not a reported fact.

## Anti-gaming Rules

Metrics must not encourage:

- premature movement of product logic into the platform;
- relabeling Product Experiments as platform reuse;
- superficial reuse that increases total cost;
- creating local authoritative copies to improve availability statistics;
- broadening a Conformance Statement to hide missing controls;
- marking requirements not applicable merely because they are inconvenient;
- retaining failed capabilities to avoid retirement;
- excessive approvals for coverage statistics;
- collecting unnecessary data to improve observability metrics;
- hiding platform delay inside product estimates;
- treating documentation volume as organizational value.

A metric should be changed or retired when it no longer represents the intended outcome.

## Review Cadence

During product validation, metrics should be reviewed at meaningful pilot, delivery, security, migration, conformance or capability-review milestones rather than through a heavy reporting process.

A fixed cadence may be introduced after stable operational data exists.

The owner of Arvectum OS may update this metric set without amending RFC-0001 when the changes remain consistent with its Platform Evidence requirements.
