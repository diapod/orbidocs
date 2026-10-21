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
- implement finite script-backed C1/C2 actions plus the closed host-managed
  C3-C5 operations, C6 composition, and host-gated C7 profile,
- execute configured commands without shell interpolation,
- enforce configured working directory, script root, timeout, stdout, stderr,
  and artifact bounds,
- report per-action class availability and keep arbitrary-process C3-C7
  declarations unavailable until their platform envelopes exist,
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
- keep interactive operator consent host-owned: prompts
  reuse `inquirium.operator-question.request.v1` projected through durable
  reuse notifications, while Sensorium OS receives an audited action-catalog
  sidecar delta or a single host-verified consumed `allow-once` binding,
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

### Local Device Discovery

Based on:
- [P045 local device discovery continuation](../../40-proposals/045-sensorium-local-enaction-stratum.md#local-device-discovery-continuation)
- [P055 private progress continuation](../../40-proposals/055-bounded-deferred-operation-contract.md#41-planned-local-device-discovery-progress)
- [P096 first BLE provider](../../40-proposals/096-sensorium-brainflow-connector.md#local-device-discovery-provider)

Planned contracts (not registered or implemented):
- `sensorium-device-discovery.request.v1`
- `sensorium-device-discovery-candidate.v1`
- `sensorium-device-discovery-result.v1`
- `deferred-operation-status.v2`

Responsibilities:
- mediate `device.discover.ble`, `device.discover.usb-serial` and
  `device.discover.mdns` through existing `sensorium.directive.invoke`,
  action-scoped admission and an independently registered bounded provider;
- distinguish external device detection from the implemented middleware
  connector discovery/routing above;
- keep discovery, host-approved binding and acquisition consent separate;
- enforce admitted passive/active effects, shared transport claims and
  same-controller scan/acquisition exclusion before I/O;
- expose caller-private, bounded replacement candidate snapshots through
  versioned S029 progress, with no candidate history or retained-list digest;
- approve/consume candidates atomically only after confirmed session cleanup,
  while preserving manual P096 binding without a scan;
- keep Interfaces catalogue/publication and scheduler repeat policy separate.

Status:
- `planned`; no available action or capability entry is added by this design.

The single common implementation tracker is **P045-DISC-001–007**. P055-10/11
own the required S029 version/retention work; P096-017/018 own the first BLE
provider and exact deployment qualification. USB/serial and mDNS are common
contract fixtures with runtime explicitly deferred. Existing hard-MVP
Sensorium capabilities and P096-002/003/004 completion remain unchanged.

[P096's finite same-candidate qualification bootstrap](../../40-proposals/096-sensorium-brainflow-connector.md#same-candidate-finite-qualification-bootstrap)
defines a private experiment boundary before authority-bearing implementation.
It reuses normal signed materialization, supervision, claims and protected wearer
control while keeping ordinary action routes closed. Immutable source facts,
independent qualification and explicit adoption are distinct; no experiment,
fixture or installed report alone makes this planned discovery action available.

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

Proposed wearable extension:
[P096: Sensorium BrainFlow Connector](../../40-proposals/096-sensorium-brainflow-connector.md)
specifies `health-wearable` profiles for non-invasive physiological measurement,
independent device instances, acquisition consent and
bounded signal projections. Its tracker owns the new implementation and real-device
qualification work. P096-003 creation/restoration and P096-004 device-free
catalogue/private binding management are implemented in Node, with no discovery
or acquisition authority. Lifecycle mutation, signal delivery, real OS/TCC
access and hardware qualification retain their gates; the status of this
connector class remains `deferred`.

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

### Reusable Bounded HTTP(S) Fetch Host Boundary

Based on:
- `doc/project/40-proposals/084-sensorium-web-observation-connector.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`

Related schemas:
- `bounded-http-fetch-request.v1`
- `bounded-http-fetch-result.v1`
- `bounded-http-fetch-artifact-read-request.v1`
- `bounded-http-fetch-artifact-read-result.v1`
- `bounded-http-fetch-error-codes.v1`
- `bounded-http-fetch-operator-snapshot.v1`
- `sensorium-web-source.v1`
- `sensorium-web-extraction-request.v1`
- `sensorium-web-document-blocks.v1`
- `sensorium-web-extraction-result.v1`
- `sensorium-web-document-snapshot.v1`
- `sensorium-web-durable-source.v1`
- `sensorium-web-refresh-claim.v1`
- `sensorium-web-refresh-status.v1`
- `sensorium-web-refresh-sweep.v1`
- `sensorium-web-refresh-sweep-outcome.v1`
- `sensorium-web-operator-snapshot.v1`
- `sensorium-web-latest-state.v1`

Responsibilities:
- expose `http.fetch.bounded` only as a host-local, non-advertisable,
  non-passportable capability for exact middleware consumers and actions;
- keep DNS resolution under a 64-address answer cap, bracket-normalized IPv6,
  IPv4-compatible/mapped and standard/local-use NAT64 classification,
  internally timed resolver attempts, bounded worker/queue backpressure,
  fresh per-hop connection pinning, explicit rustls/WebPKI TLS, exact redirect
  statuses, per-hop and total deadlines, independent header count/byte caps,
  body caps, and concurrency in the daemon;
- return bounded inline bytes or one Artifact Delivery pointer, and permit only
  a content-bound continuation under the same caller, action, artifact ref,
  digest, and size; exact bounded tombstones distinguish an evicted transfer as
  `artifact-transfer-expired` while unknown or altered bindings remain
  `artifact-binding-mismatch`, without exposing sockets, resolvers, cookie jars,
  credentials, or raw URL diagnostics;
- run the channel-only Python static extractor under the frozen
  `sensorium-web-extraction:static-stdlib-main-v1` identity, with no HTTP, DNS,
  socket, or subprocess fallback and bounded inert document blocks;
- keep extraction, source scheduling, observation admission, and interface
  publication outside the reusable host primitive; P084's closed static media
  set is enforced by `sensorium-web-core` before extraction rather than by the
  consumer-neutral fetch host.

Status:
- `done` for the static public-web macOS profile. The daemon-owned fetch boundary and its deterministic local
  conformance harness are implemented with P084 as the first configured
  consumer. The canonical nested source envelope round-trips through the pure
  Rust contract; all twenty contracts are Schema Gate-registered; daemon
  ingress/egress integration plus resolver concurrency and shutdown are covered
  without public egress; and the supervised extractor passes a thirteen-check
  offline corpus including deterministic parser-event/depth ceilings,
  content-bound artifact transfer, and capability-withheld
  refusal. The macOS Seatbelt adapter now admits only the exact host-created
  middleware endpoint; portable harness tests and automated macOS deployment
  evidence prove direct socket, DNS, proxy, and subprocess refusal. A bounded
  SQLite source runtime, exact conditional refresh, Replay Scheduler sweep,
  daemon-owned bounded P055 refresh execution with exact claim-timeout binding,
  post-claim compensation, up-to-16-source deadline-bounded sweeps,
  nonblocking shutdown, and synchronous post-connector-readiness, pre-scheduler
  keyset restart reconciliation, Sensorium
  observation admission, metadata-only operator projection, and optional P082
  latest-state adapter are implemented. Retained representations now cross an
  authenticated content-bound `artifact.delivery.retain` boundary and their P081
  receipt is chained into the Sensorium observation receipt; retained bytes are
  omitted from both the observation envelope and the SQLite cache projection.
  The single-URL operator runner in `node:tools/acceptance/sensorium-web-url/`
  uses the real daemon/channel path and reads the admitted inline representation
  through `sensorium.observation.get`, with exact source/snapshot/digest bindings
  and bounded process cleanup. Its deterministic offline mode uses the real
  connector/store with explicit host fetch/admission doubles. Declared API routes
  make source operations and health/readiness reachable through the existing
  operator bridge, with resolvable OpenAPI schema URNs. The runner checks both
  node-wide projections and the documentation shell. Sandbox environment clearing
  precedes explicit launch values and host channel bootstrap; profile values and
  temporary-variable removal are enforced afterwards in channel and stdio paths.
  The DNS deadline timer is constructed inside its owning Tokio runtime.
  Dedicated macOS local P082 acceptance now verifies real admitted snapshots
  through authenticated read and SSE, unchanged/changed content, grant revocation,
  typed generation fencing, and explicit supersession requiring a fresh grant.
  Four explicit refreshes account for all host fetches and fixture requests;
  consumers add no fetches. Evidence is retained in
  `node:docs/evidence/sensorium-web/SENSORIUM-WEB-LOCAL-INTERFACE-EVIDENCE.md`.
  Dedicated direct-peer/Room acceptance now also verifies signed read/subscription
  over the real daemon TLS peer session, dual-authority Room snapshots, revocation,
  generation fencing, supersession with fresh grants, and remote-refresh refusal.
  The Room fixture uses local WebSocket and admitted membership facts; it does not
  claim remote membership issuance or federated relay. Evidence in
  `node:docs/evidence/sensorium-web/SENSORIUM-WEB-REMOTE-INTERFACE-EVIDENCE.md` closes P084-008 with
  four explicit refreshes, four host calls and eight HTTP hops. Profile 1.2.0
  strips query values from published links under a new content-bound identity;
  old persisted profiles refuse before host effects and require an explicit new
  generation. Canary checks cover operator/carrier data and retained artifacts,
  including 100 files, 31 databases and 274 rows without leakage.
  `node:docs/evidence/sensorium-web/SENSORIUM-WEB-STATIC-ACCEPTANCE-EVIDENCE.md` closes P084-009 with
  full declared store capacity, 5,120 refreshes, 128 recovered claims, eight
  SIGKILL barriers, real HTTP overload/failures, BDO recovery and a separate
  successful randomseed probe. Static P084-001–009 are done; browser, credentials,
  crawl and broader P078 integration remain deferred. P084-012a adds explicit
  same-Node, grant-admitted snapshot intake into the local Harvester review
  registry, preserving source classification and artifact provenance without
  acquisition or publication authority. Its measured acceptance is tracked in
  `node:docs/evidence/sensorium-web/SENSORIUM-WEB-HARVESTER-EVIDENCE.md`. This does not claim non-macOS
  isolation or multi-host Room deployment.

### P084-012a review hardening

Review H-1 through H-10 distinguishes pre-claim `not-started` refusal from
settling an already claimed operation, using the same refresh-status contract
and failure semantics. A bounded refusal projection isolates the rejected
source generation and makes its reason visible without consuming operation
slots or starving healthy sources. The 1.2.1 extraction revision computes link
truncation after deduplication. Harvester configuration equality is semantic;
no-op registration returns HTTP 200. Safe host trace categories preserve refusal
causes, and the post-artifact read uses its own causal child operation without
extending the original deadline. Evidence:
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-HARVESTER-REVIEW-EVIDENCE.md`.

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

The consent endpoint host-shapes Sensorium OS choices to exactly `deny`,
`allow-once`, and `remember-action-catalog-entry`; the registry independently
validates that shape and source/capability binding. Catalog status carries a
non-authorizing history of pending, one-shot, denied, expired, revoked, inactive,
and effective approvals plus the effective catalog hash. The status sidecar is
bounded to the newest 512 approvals and diagnoses truncation; only active durable
entries contribute execution authority.

This solution owns the host-side consent state machine boundary and the shared
sidecar-merge rule; adapter-specific projection shapes are owned by their
respective solution/proposal documents, such as Sensorium OS action-catalog
deltas and Workbench command-profile deltas.

### P084-012b local review boundary

After P084-012a admission, the operator can supply an explicit redacted summary,
topic, optional polarity and draft intent through the local Harvester web review
API. `weak-signal-web-review.v1` binds this immutable decision to the original
finding digest; classification and snapshot provenance survive into an optional
unpublished local Whisper draft. This consumes already admitted local evidence
and grants no new P082 read, acquisition, remote delivery or publication authority.
The bounded v3 review store records facts and projections atomically and rebuilds
divergent review projections on reopen while validating retained facts. Explicit
FK enforcement preserves parent bindings; safe HTTP classes distinguish invalid
input, conflicting decisions, retained capacity and host failures. See P084 section "P084-012b: explicit web review and
local draft" and `node:docs/evidence/sensorium-web/SENSORIUM-WEB-REVIEWED-DRAFT-EVIDENCE.md` for the
contract, compatibility limits and measured acceptance. P084-012b is done for
this bounded local slice. Broader P084-012 remains
partial; the new slice does not close P078-007.


### P084-012c operator review projection

The node-ui review surface consumes already imported findings and sends explicit
operator decisions through the P084-012b API. Classification, provenance and the
finding digest remain visible; draft creation requires an affirmative choice.
Authentication and CSRF remain at the operator UI boundary and the daemon retains
review authority, immutable facts and the unpublished local draft. The UI grants
no fetch, P082 read or Whisper publication authority. Broader P084/P078 integration
remains partial. P084-012c is done for measured local operator UI acceptance; see
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-REVIEW-UI-EVIDENCE.md`.

### Independent safety evidence scope (2026-10-21)

The Node-local exporter and independent qualifier now have a separate P096-005
scope. It requires all ten unchanged host-boundary cases in one exact full
deployment tuple, including native origin and current firmware/TCC observations.
The full p21 exposure scope continues to require sixteen native plus ten safety
cases. Neither a partial campaign nor the new safety-only decision supplies
native transport qualification, adoption, P096-011a or release readiness.
The protected stop receipt/fence/exact-exit limits remain 250/100/5000 ms.
This is implemented software conformance; device qualification remains partial.
See `node:docs/audits/REVIEW-SENSORIUM-SAFETY-EXPORT-2026-10-21.md`.

### Accountable call and exact child witnesses (2026-10-21)

Node's normal acquisition worker now observes SDK boundary entries and successful
returns with bounded raw clocks; its source class is still separate from
qualification origin. The normal supervisor supplies a retained exact owned
launch/generation, and the acquisition owner records a conservative exit
observation only after reaping that same launch. Unknown or existing process
groups are not replaced with zero descendants. Exit never attests native release.
The device-free tests establish software conformance, not fresh firmware/TCC,
physical native qualification or adoption. Existing target packages/clients are
not upgraded in place. P096-005 remains partial.

### Completed owner-fact exporter (2026-10-21)

The offline Node exporter now projects retained owner measurements into the ten
existing P096-005 case types. It derives result/budget/control summaries, checks
exact source/run/harness/tuple/Case bindings and corroborates actual native,
private-control, fault and host-software witnesses before the unchanged Schema
Gate and semantic gates permit publication. Raw restart observation stays separate
from the original Case. Missing observations yield explicit partial coverage;
no source label, readiness, bool or historical firmware/TCC note fills a gap.
Its own source closure and consumed evidence refs are retained independently of
the standard-library-only qualifier. Full p21 still requires sixteen additional
native transport cases; software exporter completion does not complete P096-005,
native exposure, launchd scope, P096-011a or release acceptance. No hardware,
reset, recovery, target mutation or branch integration occurred.

Final containment review requires the captured actually enforced no-fork adapter
before group absence can supply a zero-descendant observation. A declarative
flag without that adapter, EPERM or an existing group keeps the fact unknown.
This restriction preserves the original qualification requirements.


### Frozen safety-export client preparation (2026-10-21)

A new Node client handoff freezes the complete offline exporter/qualifier sibling
closure and a separately pinned content-only Schema Gate alongside its signed
application. The offline projection consumes retained owner facts and does not
start a scan or acquisition. Old handoffs keep their original readers; existing
registered workers are never substituted by client preparation. Separate reviewed
package transition, current authority and fresh applicable operator decisions
remain prerequisites to native observation. The device-free checks and prepared
client do not complete P096-005 or native transport/launchd qualification.
See `node:docs/audits/REVIEW-SENSORIUM-SAFETY-CLIENT-PREPARATION-2026-10-21.md`.


The target preparation now binds corrected Node source `065bd6fb`, source pin
`1713fa35`, release `f734f50a`, signed GUI `bdd1016a` and handoff `68d332ae`.
All 244 frozen software checks pass locally and on target Python 3.13.15, with
exact file/signature/Gate and rootless GUI launchd verification. All 438 prior
root files, journal/history, expired authority and controller custody remain
unchanged; only the new capsule is added. The existing worker remains unchanged
and differs from the new SDK-observation source. A separate reviewed package
transition is required before later native measurement. No Bluetooth, grant
renewal, recovery, root migration, hardware qualification or merge occurred.


### Immutable SDK-observation package transition (2026-10-21)

The normal Node package owner now publishes separately signed ordinary/campaign
SDK-observation generations, preserving earlier package/review/sidecar/capsule
bytes. Exact retirement of the recovered expired revision 7 reserves revision 8
without reusing consent or creating an acquisition grant. Independent signature
and preimage checks, current compiled package selection, the frozen exporter/Gate
client and 244 device-free target checks pass. Prepared source `b4bc9862` / pin
`1cda5c5f`, release `c33ac91d`, GUI `d21848bb` and handoff `0b768e43` are distinct
from all historical native observations.

A separately reviewed delegated controller/discovery renewal has the unchanged
same scope and four-hour ceiling, ending 2026-10-21 18:06:05 CEST. Package approval,
retirement and finite authority remain separate from fresh SCAN/BIND/REGISTER/WEAR,
actual TCC access and measured qualification. No hardware, reset/recovery, root
format migration, merge or P096-005 completion follows. See
`node:docs/audits/REVIEW-SENSORIUM-WORKER-TRANSITION-2026-10-21.md` for exact
publication, ordinary journals and retained custody differences.


### Revision-8 measured campaign (2026-10-21)

Revision-8 physical SSH campaign on source b4bc9862/pin 1cda5c5f completed baseline and protected stop, then stopped during the deadline episode on timer-lane validation 273 ms against the original 250 ms gate. Protected receipt/fence/exact-exit measured 1/0/4717 ms; all three sessions released with current durable audit and zero claims. SDK entry/return and exact exit witnesses are now present. Three unbound collector episodes supply no formal cases; TCC attribution/full tuple and remaining safety witnesses are still missing. No retry/recovery/merge followed; P096-005 remains partial. See node:docs/audits/REVIEW-SENSORIUM-R8-CAMPAIGN-2026-10-21.md.


### Prospective control-budget revision 2 (2026-10-21)

Operator-approved future budget revision 2 sets live validation/receipt/fence to 313/313/125 ms (ceil 312.5), retaining 5000-ms exit and all other clocks/origin/tuple gates. Purpose and safety qualifier identities are v2; current purpose admission rejects the historical identity even with a substituted current artifact hash. Frozen r8 observations retain 250/100/5000 ms and remain partial. No target deployment, root/grant change, retry or merge follows. See node:docs/audits/REVIEW-SENSORIUM-CONTROL-BUDGET-V2-2026-10-21.md.


### Merged budget-v2 client preparation (2026-10-21)

Merged source 351861c9/pin e55f71a9 now has a verified nearby budget-v2 release b8bf7e8f, signed GUI 3be08e12 and handoff 59362613. Validation/receipt/fence/exit ceilings are 313/313/125/5000 ms. Merged checks pass 148 Rust, 6 Gate, 245 local and 245 nearby frozen-client cases; 22 ledger checks also pass. Exact old root/custody, journal 158 and zero claims remain unchanged; only the new capsule is added. Both temporary worktrees are retained after the approved initial merges; preparation records remain unmerged. No Bluetooth, grant renewal, recovery, migration or native qualification follows. P096-005 stays partial. See node:docs/audits/REVIEW-SENSORIUM-MERGED-BUDGET-CLIENT-2026-10-21.md. Historical campaign results retain their original gates; future hardware evidence must bind this exact candidate and current v2 qualifier.
