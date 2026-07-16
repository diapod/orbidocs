# Sensorium

`Sensorium` is the node organ for local sensorimotor contact with the world.
It admits observations, mediates bounded directives, records audit outcomes,
and hides connector mechanics behind explicit host capabilities.

Sensorium is not the whole middleware system and it is not an LLM/model-policy
surface. Model-backed inquiry belongs to Inquirium. Sensorium may invoke a
bounded local action that samples, checks, transforms, or triggers one act, but
long-running model workers and provider policy belong outside Sensorium OS.

## Purpose

Sensorium exists to give the node one policy-visible boundary for contact with
external reality:

- local observations from connectors,
- intentional directives to external systems,
- audit-only directive outcomes,
- bounded artifacts produced by connector actions,
- connector discovery and dispatch through the standard host capability layer.

The solution-level responsibility is to keep connector messiness below the
organ boundary while preserving consent, minimization, auditability, and
degradation when Sensorium is absent.

## Scope

This document defines the settled solution surface for Sensorium.

It does not define:

- every possible connector class,
- public/federated Sensorium exchange,
- invasive sensor UX beyond the local active-status requirement,
- model provider policy,
- emergency activation policy,
- or a separate plugin system outside the daemon middleware host.

## Must Implement

### Sensorium Core Boundary

Based on:
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/60-solutions/000-node/000-node.md`
- `doc/project/60-solutions/019-middleware/019-middleware.md`

Related schemas:
- `sensorium-observation.v1`
- `sensorium-directive.v1`
- `sensorium-directive-result.v1`
- `sensorium-directive-outcome.v1`

Responsibilities:
- expose the consumer-facing Sensorium host capabilities,
- keep connector dispatch behind `sensorium-core`,
- apply Sensorium configuration for sensitivity classes, TTLs, action catalog,
  and publish-approval gates,
- degrade cleanly when no connector dispatcher is available,
- keep Sensorium as a node-local organ rather than a public protocol authority.

Status:
- `done`

### Observation Admission And Read Model

Based on:
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/60-solutions/015-host-owned-module-store/015-host-owned-module-store.md`

Related schemas:
- `sensorium-observation.v1`

Responsibilities:
- admit candidate observations through `sensorium.observe.submit`,
- apply sensitivity allow/quarantine decisions,
- assign `observation/id`, ingestion time, expiry, source metadata, and
  `publish_topics` metadata,
- expose bounded query, get, health, and topic-summary surfaces,
- persist admitted observations through the host-owned module store and rehydrate
  them on daemon restart.

Status:
- `done`

### Directive Invocation And Connector Dispatch

Based on:
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`

Related schemas:
- `sensorium-directive.v1`
- `sensorium-directive-result.v1`

Responsibilities:
- expose `sensorium.directive.invoke` as the public directive capability,
- resolve `action_id` against the Sensorium action catalog,
- validate caller-supplied parameters against the action's parameter schema,
- enforce action timing and publish-approval constraints,
- dispatch only through the internal `sensorium.connector.invoke` seam,
- return a result carrying outcome and observation references rather than
  connector internals.

Status:
- `done`

### Directive Outcome Audit

Based on:
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`

Related schemas:
- `sensorium-directive-outcome.v1`
- `sensorium-directive-result.v1`

Responsibilities:
- record exactly one outcome for each accepted or rejected directive invocation,
- keep directive outcomes audit-only rather than publishing them as observations,
- expose bounded audit lookup through `sensorium.audit.read`,
- persist outcomes through the host-owned module store and rehydrate them on
  daemon restart,
- link successful outcomes to admitted observations when a connector returns
  world facts.

Status:
- `done`

### Internal Connector Capability Boundary

Based on:
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/60-solutions/006-capability-binding/006-capability-binding.md`

Related schemas:
- `sensorium-directive.v1`
- `sensorium-directive-result.v1`

Responsibilities:
- keep `sensorium.connector.invoke`,
  `sensorium.connector.operation.status`, and
  `sensorium.connector.operation.cancel` internal to `sensorium-core`,
- reject direct connector invocation from ordinary middleware modules,
- route connector calls through the daemon host capability dispatcher,
- preserve connector isolation as middleware, not as a Sensorium-specific plugin
  API.

Status:
- `done`

### Sensorium OS Reference Connector

Based on:
- `doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`
- `doc/project/60-solutions/016-bounded-local-server-runtime/016-bounded-local-server-runtime.md`

Related schemas:
- `sensorium-directive.v1`
- `sensorium-directive-result.v1`
- `sensorium-os-error-codes.v1`

Responsibilities:
- run `sensorium-os` as the first supervised Sensorium connector,
- advertise `module_role = sensorium-connector` and connector action metadata,
- implement finite script-backed C1/C2 Sensorium OS actions and expose the P048
  action-class catalog,
- execute configured commands without shell interpolation,
- enforce configured working directory, script root, timeout, stdout, stderr,
  and artifact bounds,
- report per-action class availability and fail closed for unavailable C3-C7
  classes until their enforcement envelopes exist,
- use the authorized action catalog entry as the canonical executable source and
  reject request-local allowlist or host-policy overrides,
- enforce `result_pointer_fields` exact/prefix result contracts,
- reject invalid action ids, invalid result pointer identifiers, and
  allowlist-local sensitivity override or unknown sensitivity keys,
- distinguish missing or invalid authorized catalog entries from ordinary
  not-allowlisted requests with stable diagnostic codes,
- return structured results and artifact references without embedding large
  payloads into directive envelopes.

Status:
- `done`

### Sensorium OS Action Catalog Authorization

Based on:
- `doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`
- `doc/project/60-solutions/006-capability-binding/006-capability-binding.md`

Related schemas:
- none frozen

Responsibilities:
- report action catalog hash, sidecar metadata, per-action availability, catalog
  diagnostics, authorized action ids, and runtime-available action ids,
- fail closed when action catalog signature is required and missing or stale,
- let the daemon write operator-signed grant or deny sidecars from the operator
  surface,
- keep any future interactive operator consent path host-owned: prompts should
  reuse `inquirium.operator-question.request.v1` projected through durable
  notifications, while Sensorium OS receives only an audited action-catalog
  sidecar delta after the operator grants consent,
- load host-projected `sensorium-os.action-catalog-sidecar.v1` consent deltas as
  append-only, non-overriding action declarations and expose their diagnostics
  through the catalog status surface,
- keep cryptographic key use in the daemon/HostSigner stratum rather than in
  the connector.

Status:
- `done`

### Deferred Sensorium Actions

Based on:
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`
- `doc/project/60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md`

Related schemas:
- `deferred-operation.v1`
- `deferred-operation-status.v1`
- `sensorium-directive.v1`
- `sensorium-directive-result.v1`

Responsibilities:
- allow action catalog entries to opt into bounded async/deferred execution,
- map connector deferred acknowledgements into canonical host deferred
  operations,
- expose `sensorium.operation.status` and `sensorium.operation.cancel`,
- register Sensorium deferred operations in the host deferred registry,
- preserve explicit non-cancelable and terminal-state behavior.

Status:
- `done`

## May Implement

### Local Agora Observation Publication

Based on:
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/046-agora-topic-key-namespace-conventions.md`

Related schemas:
- `sensorium-observation.v1`

Responsibilities:
- publish admitted observations to local-only topics such as
  `local/sensorium/observations/{signal-kind}`,
- keep public/federated publication out of Sensorium by default,
- let consumers subscribe without coupling to connector implementation details.

Status:
- `partial`

Implementation note: current runtime records `publish_topics` metadata, stores
and rehydrates observations, and exposes query/topic-summary read surfaces. A
full local Agora subscription bus remains a later integration layer.

### Invasive Connector Classes

Based on:
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`

Related schemas:
- `sensorium-observation.v1`

Responsibilities:
- support camera, microphone, GPS, wearable, or comparable invasive connector
  classes only after active UI status and explicit operator grants exist,
- surface declared incidental effects before enabling observation or directive
  flow,
- default to disabled until the operator has accepted the connector posture.

Status:
- `deferred`

### Cross-Node Sensorium Read-Through

Based on:
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/082-sensorium-interfaces.md`
- `doc/project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md`

Related schemas:
- `sensorium-interface-descriptor.v1`
- `sensorium-interface-read-request.v1`
- `sensorium-interface-read-result.v1`
- `sensorium-interface-subscribe-request.v1`
- `sensorium-interface-subscription-status.v1`
- `sensorium-interface-frame.v1`

Responsibilities:
- delegate trusted-neighbor observation access to the exact-resource Sensorium
  Interface contract,
- preserve local consent and minimization rules,
- avoid turning Sensorium into a general remote surveillance API, where
  "surveillance" names an act — observing subjects without their knowledge or
  consent, or beyond the scope they consented to — never the mere existence of
  a remote observation capability,
- bind that guardrail to defaults and authorization, not capability: no
  ambient or default-on observation, source-side enumerability of active
  exposures and their grant holders, scoped and audited grants with effective
  end-to-end revocation, and classification (`bound_subjects`) carried for
  third-party subjects appearing in exposed representations — while never
  narrowing what a consenting operator may deliberately expose.

Status:
- `implemented` by Solution 046. Sensorium remains the owner of local observation
  admission and source policy; the Sensorium Interfaces runtime owns explicit
  publication, exact grants, pull-batch reads/subscriptions, direct-peer Passport
  admission, revocation, and carrier adapters. Local Sensorium topics remain
  non-federated.

## Out of Scope

- public/federated Sensorium publication by default,
- direct connector invocation by consumers,
- unrestricted OS access,
- long-running daemons, watchers, streams, or model workers inside
  `sensorium-os`,
- Inquirium/model provider policy,
- emergency activation decisions,
- direct network publication of Whisper, Monus, or Arca artifacts.

## Consumes

- connector module reports,
- `sensorium-observation.v1` candidates,
- `sensorium-directive.v1` requests,
- host capability bindings,
- operator-signed action catalog sidecars,
- bounded deferred operation policy.

## Produces

- admitted `sensorium-observation.v1` records,
- `sensorium-directive-result.v1` responses,
- audit-only `sensorium-directive-outcome.v1` records,
- host deferred operation handles for async connector actions,
- Sensorium health, query, topic-summary, directive-list, and audit read models.

## Related Capability Data

- `030-sensorium-caps.edn`

## Notes

Sensorium is best read as a mediated bus and policy boundary, not as an
interceptor chain. Connectors adapt external systems; `sensorium-core` admits,
normalizes, dispatches, and records; consumers use host-granted capabilities and
remain ignorant of connector mechanics.

Sensorium OS is only the first reference connector. A deployment may replace it
or run several Sensorium connector middleware modules with different action
catalogs and grants. Consumers should depend on Sensorium capabilities and
action contracts, not on a concrete connector module.

Sensorium Workbench is the separate high-impact connector/runtime component for
terminal sessions, workspace file views, patch application, and local
interactive work. Its solution-level boundary is owned by
`doc/project/60-solutions/042-sensorium-workbench/042-sensorium-workbench.md`
rather than by this core Sensorium organ document.

Interactive consent for adding new Sensorium OS actions or Workbench command
profiles is also host-owned. Sensorium connectors may request a decision, but
the prompt/answer state machine belongs to the daemon's operator-question and
notification layers; adapters receive only validated consent outcomes projected
into their own sidecar formats. The first Sensorium OS projection now exists:
durable `remember-action-catalog-entry` grants are materialized into
`sensorium-os.action-catalog-sidecar.v1` after daemon-side expiry, operator
binding, and durable-grantability checks, written to the Sensorium OS middleware
config tree, then merged by the connector only as valid non-overriding action
entries.

This solution owns the host-side consent state machine boundary and the shared
sidecar-merge rule; adapter-specific projection shapes are owned by their
respective solution/proposal documents, such as Sensorium OS action-catalog
deltas and Workbench command-profile deltas.
