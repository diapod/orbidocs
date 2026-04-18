# Orbiplex Arca

`Orbiplex Arca` is a Node-attached, demand-side solution component
that provides a **buyer-side workflow orchestrator** and the
**observed offer catalog** for buyer-side discovery. It is the
counterpart of `Dator` (the supply-side component); together the two
form the Orbiplex marketplace runtime split: `Dator` owns publication
and the responder side, `Arca` owns observation, discovery, and
buyer-side workflow orchestration.

Arca does not author signed protocol artifacts. Service-orders,
procurement contracts, settlement holds, and peer transport all
belong to host-owned capabilities exposed by the daemon; Arca
*proposes* workflow intent and consumes those host capabilities. This
boundary keeps Arca a hosted module rather than a protocol authority
(see story-006-buyer-node-components and the
service-order-to-procurement-bridge memo).

The v1 deployment runs as a supervised middleware service under the
Node daemon's `http_local_json` executor, reachable on loopback
(default `127.0.0.1:47981`), discovered by the daemon through the
standard middleware-init contract.

## Purpose

The component is responsible for the solution-level execution path of:

- normalising a configured workflow plan into a sequential,
  dependency-ordered step graph and creating a host-owned workflow
  run,
- building per-step `service-order.v1` requests, submitting them
  through the classified buyer ingress, polling execution through
  `AwaitingManualRelease`, and resolving each step to `completed`,
  `failed`, `deadline_exceeded`, or `step_timeout`,
- applying per-step retry policy with `retry_delay_ms` backoff and a
  `max_retries` cap, and per-step `fail_policy` (currently
  `abort_workflow`) when the retry budget is exhausted,
- emitting operator notifications and persisting final artifacts
  through host-owned module APIs,
- maintaining a local SQLite-backed observed offer catalog populated
  through periodic background sync against discovered catalog peers,
  inbound `offer-catalog.fetch.response` and `offer-catalog.push`
  peer messages, and on-demand remote queries correlated through a
  `threading.Event` handle,
- serving a combined participant-facing catalog view at
  `GET /v1/enact/service-catalog` merging local snapshots with
  observed remote offers,
- consuming host capabilities (`offers.local.query`,
  `seed.directory.query`, `peer.session.establish`,
  `peer.message.dispatch`) for all peer transport and discovery,
  rather than opening its own peer sockets.

## Scope

This document defines solution-level responsibilities of the Arca
component.

It does not define:

- the supply-side responsibilities owned by `Dator` (local
  standing-offer publication, provider-side
  `offer-catalog.fetch.response` answers, outbound `offer-catalog.push`
  emission for local offers),
- daemon-owned protocol authority (signing service-orders, opening
  procurement, performing settlement holds, peer transport, capability
  passport issuance) — Arca consumes these through host capabilities,
- per-kind semantic interpretation of service outputs — that lives in
  the per-service schema and the consumer module,
- the editorial, content, or research semantics of any specific
  workflow template (e.g. story-009 `bielik-biweekly-publish.v1`) —
  Arca only provides the orchestration substrate.

## Must Implement

### Workflow Run Orchestration

Based on:
- `doc/project/30-stories/story-006.md`
- `doc/project/30-stories/story-006-buyer-node-components.md`
- `doc/project/20-memos/service-order-to-procurement-bridge.md`
- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`

Related schemas:
- `service-order.v1`
- `procurement-contract.v1`
- `procurement-receipt.v1`

Responsibilities:
- normalize a configured workflow plan into a sequential,
  dependency-ordered step graph (`depends_on`, `input_from`),
- create a host-owned workflow run and update step status snapshots
  through the daemon module API,
- build per-step `service-order.v1` requests from configured
  `request_input` plus upstream step output references,
- submit one service-order per step through the classified buyer
  ingress at `POST /v1/service-orders`,
- poll execution state through `AwaitingManualRelease` and resolve to
  `completed`, `failed`, `deadline_exceeded`, or `step_timeout`,
- apply per-step retry policy with `retry_delay_ms` backoff and
  `max_retries` cap; honor `fail_policy` (currently `abort_workflow`)
  on retry-budget exhaustion,
- emit operator notifications via `POST /v1/module/notify` and
  persist final artifacts via `POST /v1/module/artifact/write` under
  host-owned module output roots,
- resume a previously persisted workflow run on module restart.

Status:
- `partial` in the bundled middleware module. Sequential
  single-target workflow with retry, dependency-ordered
  `input_from` chaining, persisted run state, notifications, and
  artifact writes are live. Task-type-targeted ordinary steps now
  flow through the same service-order path: `target.resolve =
  task_type` without `fan_in` is treated as provider selection, not
  host-managed fan-out; `target.task_type` maps to offer-catalog
  `service/type` when no explicit `service_type` is provided.
  Proposal-033 temporal shape is preserved (`deadline`,
  `timing.timeout`, `timing.on_timeout`); legacy `deadline_seconds`
  is rejected on template instantiation. Full non-fan-out
  `timing.timeout` enforcement is still pending.

### Observed Offer Catalog and Discovery

Based on:
- `doc/project/30-stories/story-006.md`
- `doc/project/30-stories/story-007.md`
- `doc/project/40-proposals/023-federated-offer-distribution-and-catalog-listener.md`

Related schemas:
- `service-offer-relay.v1`
- `trusted-provider.v1`

Responsibilities:
- persist observed remote offers in a local SQLite-backed catalog
  with a per-source trust level,
- discover offer-catalog peers through the daemon host capability
  surface (`offers.local.query`, `seed.directory.query`,
  `peer.session.establish`, `peer.message.dispatch`),
- run a periodic background sync against discovered catalog peers
  (`peer_sync_interval_sec`),
- accept inbound `offer-catalog.fetch.response` and
  `offer-catalog.push` peer messages, validate them, and upsert,
- issue on-demand remote catalog queries (`POST catalog/remote-query`)
  and correlate the asynchronous responses through a
  `threading.Event` handle,
- serve the combined participant-facing catalog view at
  `GET /v1/enact/service-catalog` merging local snapshots with
  observed remote offers,
- apply `trusted_providers` policy when admitting observed offers.

Status:
- `done` in the bundled middleware module. Observed catalog storage,
  trusted-provider policy, peer discovery and background sync,
  fetch.response / push admission, on-demand remote query, and the
  combined catalog view are live (see
  `node/docs/IMPLEMENTATION-LEDGER.md` proposal 023 row).

### Host Capability Bridge Consumer

Based on:
- `doc/project/20-memos/node-middleware-init-and-capability-reporting.md`
- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/40-proposals/027-middleware-peer-message-dispatch.md`

Related schemas:
- `middleware-init.schema.json`
- `middleware-module-report.schema.json`
- `peer-message-invoke.v1.schema.json`
- `local-input-invoke.v1.schema.json`

Responsibilities:
- run as a supervised `http_local_json` middleware module under the
  daemon, with module config layered from
  `ORBIPLEX_MIDDLEWARE_CONFIG_DIR` and
  `ORBIPLEX_NODE_CONFIG_DIR`,
- declare `input_chains` for `inbound-local` routes
  (`GET service-catalog`, `POST catalog/remote-query`) and for
  `inbound-peer` message types (`offer-catalog.fetch.response`,
  `offer-catalog.push`),
- consume the host-owned `authtok` and `middleware_home` env
  contract,
- use host capability endpoints for all peer transport, never opening
  its own outbound peer sockets.

Status:
- `done` in the bundled middleware module.

## May Implement

### Workflow Template Instantiation

Based on:
- `doc/project/40-proposals/029-workflow-template-catalog.md`
- `doc/project/40-proposals/044-host-owned-generic-module-store.md`
- `doc/project/30-stories/story-009-bielik-blog-arca.md`

Related schemas:
- `workflow-template.v1` (proposed)

Responsibilities:
- accept `template_id` plus operator-supplied parameters and produce
  a concrete `WorkflowDefinition` ready to dispatch,
- resolve templates from a local template store. The current host-owned
  substrate is the Node module store, using `record_kind =
  workflow-template`; Arca owns the payload schema and instantiation
  semantics,
- optionally browse and import templates from a public template
  catalog peer.

Status:
- `partial` — the local path is implemented. Arca stores workflow
  templates in the host-owned module store (`record_kind =
  workflow-template`), accepts `template_id` plus parameters, renders a
  concrete normalized `WorkflowDefinition`, and can either return that
  materialized definition or start a host-owned workflow run from it.
  Public/federated template catalog publication, browsing, fetch, and
  import remain deferred.

### Workflow Fan-Out and Aggregation

Based on:
- `doc/project/40-proposals/033-workflow-fan-out-and-temporal-orchestration.md`
- `doc/project/30-stories/story-006.md`

Related schemas:
- `service-order.v1`

Responsibilities:
- express a step that dispatches one request to multiple discovered
  targets simultaneously,
- wait for responses according to a configurable aggregation policy
  (first / any / all / quorum),
- collect and select per the configured fan-in policy and surface the
  selected output to the next step.

Status:
- `partial` — the thin host-managed fan-out slice exists for explicit
  `target` + `fan_in` steps. The daemon resolves static and
  protocol-capability targets, persists `WorkflowStepDispatch` records,
  reconciles `any_one`, `all`, and implemented-but-deferred
  `best_of`, and surfaces inspection data in
  `WorkflowRunSnapshot.steps[].dispatches`. Quorum and retry/backoff
  policies remain deferred.

### Workflow Temporal Orchestration

Based on:
- `doc/project/40-proposals/033-workflow-fan-out-and-temporal-orchestration.md`

Responsibilities:
- honor per-step `timing.timeout` / `timing.on_timeout` and emit
  `step_timeout` when exceeded,
- honor a workflow-run-level `deadline` and emit `deadline_exceeded`
  when exceeded,
- express retry with explicit backoff and a `max_attempts` cap at the
  `WorkflowDefinition` layer.

Status:
- `partial` — workflow-level `deadline` and fan-out step-level
  `timing.timeout` / `timing.on_timeout` are implemented in daemon
  fan-out reconciliation. Ordinary non-fan-out service-order steps still
  use Arca polling/retry and do not yet enforce `timing.timeout`.

### Workflow Target Resolution by Task Type

Based on:
- `doc/project/30-stories/story-009-bielik-blog-arca.md`
- `doc/project/30-stories/story-000.md`

Responsibilities:
- express ordinary service-order step targets as `resolve: task_type`
  with a `task_type` rather than a hard-coded participant,
- at dispatch time, use the host/catalog lookup surface to resolve the
  current offer/provider for the mapped `service/type`, then continue through
  the ordinary service-order path.

Status:
- `partial` — ordinary Arca execution accepts `target.resolve =
  task_type`; when `service_type` is omitted, `target.task_type`
  becomes the service lookup key. A task-type target with no `fan_in`
  does not trigger host-managed fan-out. Dedicated richer task-type
  lookup/filter semantics remain open beyond the phase-0 slice.

### Peer Workflow Fan-Out Bridge

Based on:
- `doc/project/40-proposals/033-workflow-fan-out-and-temporal-orchestration.md`

Responsibilities:
- accept inbound peer workflow fan-out requests and process them as
  ordinary local catalog queries.

Status:
- `partial` — `handle_peer_workflow_fanout_request` exists as a
  stub-style handler returning a classified outcome.

## Out of Scope

- local standing-offer publication and provider-side
  `offer-catalog.fetch.response` answers — those belong to `Dator`,
- authoring or signing service-orders, procurement contracts, or
  receipts — those go through host-owned capabilities,
- settlement, balance precheck, and hold management — host-owned
  through the deployment-local settlement write gate,
- per-kind semantic interpretation of service outputs,
- offer relay transport and peer session establishment — those are
  daemon host capabilities consumed by Arca, not owned by it,
- editorial, research, or content semantics of any specific
  workflow template (e.g. story-009).

## Consumes

- `service-offer-relay.v1`
- `trusted-provider.v1`
- `peer-message-invoke.v1`
- `local-input-invoke.v1`
- `middleware-init.schema.json`

## Produces

- `service-order.v1`
- `catalog-local-query-request.schema.json`
- `catalog-local-query-response.schema.json`

## Related Capability Data

- `arca-caps.edn`

## Notes

Arca is bundled as a supervised Python middleware module under the
`http_local_json` executor; the bundled implementation lives at
`node/middleware-modules/arca/` (see the module's `README.md`,
`service.py`, and `config/00-arca.json`). The Arca/Dator split is the
deployment model — the legacy `offer_catalog.enabled` flag has been
removed, and `Dator` is the supply-side counterpart for local offer
publication and responder-side fetch/push.

Arca's MUST boundary is intentionally narrow: it orchestrates and it
discovers, but it does not author signed acts. Every signed protocol
artifact (service-order ingress, procurement open, settlement hold,
peer dispatch) is reached through a host capability surface owned by
the daemon. This is what makes Arca a *hosted* workflow module rather
than a parallel protocol authority — see the
service-order-to-procurement-bridge memo for the canonical statement
of what Arca may and may not do.

Story-009 (`bielik-biweekly-publish.v1`) is the first story that
exercises Arca beyond the story-006 single-vertical-slice profile. It
requires three currently non-`done` capabilities:
`workflow-template-instantiate` (`:todo`),
`workflow-target-by-task-type` (`:partial`), and the per-step subset of
`workflow-temporal-orchestration` (`:partial`). Until those land, the
story-009 sequence cannot be expressed in a `WorkflowDefinition` that
Arca can dispatch end-to-end.
