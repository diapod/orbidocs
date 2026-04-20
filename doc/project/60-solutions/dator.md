# Orbiplex Dator

`Orbiplex Dator` is a Node-attached, supply-side marketplace solution
component. It owns local standing-offer publication, provider-side
catalog answers, and provider-side service dispatch. It is the
counterpart of `Arca`: `Dator` supplies offers and executes accepted
work, while `Arca` observes catalogs, selects offers, and orchestrates
buyer-side workflows.

Dator does not own settlement, procurement authority, peer transport,
or buyer-side discovery. Those remain host-owned daemon capabilities or
Arca responsibilities. This keeps Dator a hosted supply module rather
than a protocol authority.

The v1 deployment runs as a supervised middleware service under the
Node daemon's `http_local_json` executor, reachable on loopback
(default `127.0.0.1:47971`), discovered through the standard
middleware-init contract.

## Purpose

The component is responsible for the solution-level execution path of:

- committing local standing offers for the provider participant,
- maintaining deterministic `offer/id`, monotonic `sequence/no`, and
  provider context for offers it owns,
- handling participant-facing local publication through
  `POST /v1/enact/participant/service-offers`,
- answering `offer-catalog.fetch.request` with local offers only,
- exposing a daemon-facing local offer snapshot for local dispatch
  lookups,
- accepting `service_dispatch_execute` payloads for local provider
  work,
- routing executable offers to configured local role modules,
- answering peer `service-order.dispatch.request` by executing the same
  local role-module path and returning `service-order.dispatch.response`,
- refreshing its own `offer-catalog` capability passport through host
  capabilities.

## Scope

This document defines solution-level responsibilities of the Dator
component.

It does not define:

- observed-offer storage, trusted-provider policy, peer catalog
  discovery, or combined buyer catalog reads — those belong to `Arca`,
- peer session establishment, generic peer message dispatch, passport
  issuance, and participant signing — those are daemon host
  capabilities,
- procurement contract creation, settlement hold creation/release, or
  receipt signing — those are host-owned marketplace and settlement
  paths,
- task semantics for a concrete work type — those belong to the role
  module selected by the Dator offer,
- Sensorium connector selection — role modules may request
  `sensorium.directive.invoke`, but Sensorium-core remains the
  admission and connector-selection authority.

## Must Implement

### Supply-Side Standing Offer Publication

Based on:
- `doc/project/30-stories/story-006.md`
- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`
- `doc/project/40-proposals/023-federated-offer-distribution-and-catalog-listener.md`

Related schemas:
- `service-offer.v1`
- `participant-service-offer-publish-request.schema.json`
- `participant-service-offer-publish-response.schema.json`
- `service-offer-relay.v1`

Responsibilities:
- own the local standing-offer write path for provider-side offers,
- derive deterministic `offer/id` values for managed offers,
- assign monotonic `sequence/no` values for offer updates,
- inject provider participant and provider node context,
- accept participant-facing local publication requests,
- return `published` once the local commit succeeds,
- treat outbound relay as best-effort metadata separate from local
  publication success,
- honor relay hints such as `relay.do_not_forward` and
  `relay.intended_node_id` without making them catalog semantics.

Status:
- `done` for the hard-MVP local publication path. Dator owns the local
  write, while the daemon remains transport and commit-log authority.

### Provider Catalog Responder

Based on:
- `doc/project/30-stories/story-006.md`
- `doc/project/40-proposals/023-federated-offer-distribution-and-catalog-listener.md`

Related schemas:
- `service-offer.v1`
- `service-offer-relay.v1`

Responsibilities:
- answer inbound `offer-catalog.fetch.request` with local offers only,
- keep responder behavior supply-side and stateless with respect to
  observed remote catalogs,
- expose `POST /v1/enact/offers/snapshot` for daemon-side local dispatch
  lookups,
- refresh the provider's `offer-catalog` capability passport through
  the host,
- avoid peer discovery and background pull responsibility.

Status:
- `done` in the bundled Dator module.

### Provider Service Dispatch

Based on:
- `doc/project/30-stories/story-006.md`
- `doc/project/30-stories/story-009-bielik-blog-arca.md`
- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`
- `doc/project/40-proposals/027-middleware-peer-message-dispatch.md`

Related schemas:
- `service-dispatch-request.schema.json`
- `service-dispatch-response.schema.json`
- `peer-message-invoke.v1.schema.json`

Responsibilities:
- accept daemon-submitted `service_dispatch_execute` payloads for
  local provider work,
- select the matching standing offer by `service_type`,
- route executable offers through `dispatch.kind = role-module`,
- invoke the configured role host capability identified by
  `dispatch.capability_id`,
- preserve workflow lineage fields such as `workflow/run-id`,
  `workflow/phase-id`, and `correlation/id`,
- return pointer-sized service-dispatch responses suitable for Arca and
  procurement inspection.

Status:
- `done` for the hard-MVP local and story-009 role-module path.

### Peer Service-Order Dispatch Responder

Based on:
- `doc/project/30-stories/story-009-bielik-blog-arca.md`
- `doc/project/40-proposals/027-middleware-peer-message-dispatch.md`

Related schemas:
- `service-dispatch-request.schema.json`
- `service-dispatch-response.schema.json`
- `peer-message-invoke.v1.schema.json`

Responsibilities:
- accept inbound peer `service-order.dispatch.request`,
- execute the enclosed dispatch payload through the same local
  role-module path used by local provider dispatch,
- correlate the response by `request_id`,
- return `service-order.dispatch.response` without changing the domain
  dispatch contract.

Status:
- `done` for the current peer-message remote-provider slice.

### Host Capability Bridge Consumer

Based on:
- `doc/project/20-memos/node-middleware-init-and-capability-reporting.md`
- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/40-proposals/027-middleware-peer-message-dispatch.md`

Related schemas:
- `middleware-init.schema.json`
- `middleware-module-report.schema.json`
- `local-input-invoke.v1.schema.json`
- `peer-message-invoke.v1.schema.json`

Responsibilities:
- run as a supervised `http_local_json` middleware module under the
  daemon,
- consume the host-owned `authtok` and `middleware_home` env contract,
- declare handled service types and inbound routes through
  middleware-init/module-report,
- use host capabilities for passport issuance, peer dispatch, and role
  capability invocation,
- never open its own peer transport sockets.

Status:
- `done` in the bundled middleware module.

## May Implement

### Provider Queue and Backpressure

Based on:
- `doc/project/30-stories/story-006.md`
- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`

Related schemas:
- `service-order.v1`
- `service-dispatch-request.schema.json`

Responsibilities:
- persist incoming accepted provider dispatches before execution,
- enforce `queue_max_depth` as local admission/backpressure instead of
  relying only on buyer-side pre-contract rejection,
- expose queue depth and dispatch status for operator inspection,
- run one or more worker loops with explicit timeout and retry policy,
- keep admission idempotent by `order/id` or dispatch id.

Status:
- `planned`. Current config carries `queue_auto_accept`,
  `queue_max_depth`, and `queue_current_depth`-style metadata, but the
  bundled Dator path still executes accepted dispatches inline rather
  than through a durable provider queue.

### Durable Offer Relay Outbox

Based on:
- `doc/project/40-proposals/023-federated-offer-distribution-and-catalog-listener.md`

Related schemas:
- `service-offer-relay.v1`

Responsibilities:
- persist outbound relay attempts for locally published offers,
- retry failed delivery under bounded policy,
- expose delivery state separately from local publication state,
- preserve `relay.do_not_forward` and `relay.intended_node_id` as
  relay-policy metadata.

Status:
- `partial`. Local publication and best-effort relay dispatch exist;
  a durable retryable outbox remains post-MVP.

### Public Template Catalog Participation

Based on:
- `doc/project/40-proposals/029-workflow-template-catalog.md`
- `doc/project/40-proposals/044-host-owned-generic-module-store.md`
- `doc/project/30-stories/story-009-bielik-blog-arca.md`

Related schemas:
- `workflow-template.v1`

Responsibilities:
- publish workflow templates as supply-side catalog records when a
  node intentionally hosts a template catalog role,
- list and fetch template records for remote Arca import,
- keep template publication separate from ordinary task-offer
  publication.

Status:
- `planned`. Arca has local template storage and instantiation through
  the host-owned module store; public/federated template catalog
  participation is deferred.

### Rich Provider Operator Surface

Based on:
- `doc/project/30-stories/story-006.md`
- `doc/project/30-stories/story-009-bielik-blog-arca.md`

Related schemas:
- `service-offer.v1`
- `service-dispatch-response.schema.json`

Responsibilities:
- inspect local offers with publication and relay state,
- inspect role-module routing and required Sensorium action
  declarations,
- inspect accepted, running, completed, failed, and rejected provider
  dispatches,
- expose provider-side health without leaking role-module private
  artifacts.

Status:
- `optional`. MVP exposes enough module and offer state for the current
  harnesses; richer operator UX is a post-MVP surface.

## Out of Scope

- observed catalog storage and trusted-provider policy — Arca owns the
  demand-side catalog,
- workflow orchestration and offer selection — Arca owns buyer-side
  orchestration,
- peer session establishment and generic peer dispatch — daemon host
  capabilities own transport,
- procurement, settlement, receipt signing, and release/refund/freeze
  transitions — host-owned marketplace and settlement paths,
- concrete task semantics — role modules own task-specific work,
- direct Sensorium connector invocation — Sensorium-core mediates
  connector access.

## Consumes

- `service-offer.v1`
- `service-offer-relay.v1`
- `service-dispatch-request.schema.json`
- `peer-message-invoke.v1.schema.json`
- `middleware-init.schema.json`

## Produces

- `service-offer.v1`
- `service-dispatch-response.schema.json`
- `service-order.dispatch.response`

## Notes

- Dator is bundled as a supervised Python middleware module under the
  `http_local_json` executor.
- The Arca/Dator split is the only deployment model for the current
  marketplace runtime: Dator is supply-side, Arca is demand-side.
- `service_type` names the concrete marketplace service offered by
  Dator. `task_type` remains an Arca/workflow-side selector that may
  resolve to a service type during provider selection.
- Queueing is the main remaining Dator completeness gap for provider
  execution hardening.
