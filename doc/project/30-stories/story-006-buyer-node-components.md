# Story 006 Buyer Node Components for `Arca`

Based on:
- `doc/project/30-stories/story-006.md`
- `doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`
- `doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`
- `doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`
- `doc/project/50-requirements/requirements-010.md`
- `doc/project/50-requirements/requirements-011.md`
- `doc/project/60-solutions/node.md`

Date: `2026-03-30`
Updated: `2026-04-07`
Status: Accepted hard-MVP planning note with implementation sync

## Purpose

This note distills what the buyer-side `Orbiplex Node` must implement or complete
so that a buyer-orchestrator Node can perform a marketplace purchase through the
bundled `Orbiplex Arca` middleware module.

The key architectural constraint is deliberate:

- `Arca` is a hosted workflow module,
- the Node host remains the authority for protocol artifacts, signing, settlement,
  and policy enforcement,
- therefore `Arca` must consume host-owned capabilities rather than inventing or
  mutating arbitrary wire payloads.

This document is intentionally placed before implementation. The hard-MVP buyer
path should freeze the necessary data contracts and host capability surface before
the workspace adds new execution code.

Related source artifacts created from this note:

- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`
- `doc/project/50-requirements/requirements-012.md`
- `doc/project/20-memos/service-order-to-procurement-bridge.md`
- `doc/project/20-memos/story-006-settlement-rail-sprint-3.md`
- `doc/schemas/service-offer.v1.schema.json`
- `doc/schemas/service-order.v1.schema.json`

## Implementation Status Note (`2026-04-07`)

The hard-MVP buyer path described by this note is now substantially implemented in
the `Node` workspace.

Closed in the current workspace:

- local committed `service-offer.v1` catalog with supervised publication,
- `service-order.v1` ingress and selected-offer procurement bridge,
- deployment-local settlement rail including gateway adapter MVP and hold-backed
  execution lifecycle,
- operator and UI inspection surfaces for workflow runs, settlement state, module
  registry, and execution-to-receipt joins,
- durable multi-step `Arca` orchestration over host-owned workflow state.

The remaining items called out below should therefore be read as post-hard-MVP
work unless explicitly marked otherwise.

## Non-Goals

This note does not yet:

- define the full provider-side `Dator` implementation,
- replace the current procurement substrate,
- define the full distributed service-catalog topology,
- define the complete `ORC` gateway or escrow runtime,
- define the full `Arca` workflow DSL.

## Design Constraint: `Arca` Is Not a Protocol Authority

For hard MVP, `Arca` MUST NOT:

- sign protocol artifacts,
- fabricate arbitrary `service-offer`, `procurement-contract`, or
  `procurement-receipt` payloads,
- bypass host procurement or settlement policy,
- select a different payer or provider than the host-approved workflow step,
- reach directly into gateway or escrow rails.

Instead, `Arca` should:

- propose workflow intent,
- select from host-visible catalog data,
- call host-owned ordering and inspection surfaces,
- react to bounded host results,
- and shape only those local workflow payloads that the host explicitly allows by
  contract and field policy.

## Contracts To Freeze Before Code

The buyer-side purchase slice should not be implemented before the following
contracts are written down and reviewed.

### 1. `service-offer.v1`

Needed because `story-006` is standing-offer and catalog driven.

This artifact should remain distinct from:

- `node-advertisement.v1`
- `capability-advertisement.v1`

Hard-MVP contract minimum:

- `offer/id`
- `provider/participant-id`
- `provider/node-id`
- `service/type`
- `pricing/*`
- machine-readable `pricing/unit-kind`
- `constraints/input`
- `constraints/output`
- `delivery/max-duration`
- `queue/*`
- `hybrid`
- `model-first`
- `seq`
- `ts`
- `ttl`
- `signature`

### 2. `service-order.v1`

This is the missing buyer-facing purchase intent artifact.

`service-order.v1` should describe:

- which standing offer the buyer selected,
- who the payer subject is,
- which service parameters are requested,
- what bounded output is expected,
- what economic ceiling and deadline posture are acceptable,
- and which workflow run or phase caused the order.

Hard-MVP freeze:

- `buyer/subject-kind` is limited to `participant` and `org`,
- `org` purchases carry `buyer/operator-participant-id`,
- the operational signature is performed by the custodian participant while the
  accountable buyer subject remains the organization.

This artifact should remain buyer-facing and exchange-facing. It should not expose
internal daemon execution details.

### 3. `service-order -> procurement` bridge contract

The current executable substrate in Node is still the procurement family. For hard
MVP, a buyer-side order therefore needs an explicit host-owned bridge:

- `service-order.v1`
  ->
- `question-envelope.v1` and procurement execution state
  ->
- `procurement-contract.v1`
  ->
- `response-envelope.v1`
  ->
- `procurement-receipt.v1`

This bridge contract should freeze:

- which `service-order` fields map into current procurement inputs,
- which fields are host-derived,
- which fields `Arca` may only propose rather than author,
- where settlement refs enter,
- how workflow lineage is preserved.

Hard-MVP settlement assumption:

- the bridge targets one deployment-local settlement authority boundary,
- local or co-located `gateway + escrow + catalog` deployment is acceptable,
- the buyer-side implementation should not speculate yet about a final remote
  buyer-to-escrow wire protocol.

### 4. Buyer-side ledger and funding visibility contract

The buyer Node needs a stable read-side contract over:

- `ledger-account.v1`
- `ledger-hold.v1`
- `ledger-transfer.v1`
- `gateway-receipt.v1`

This should answer, at minimum:

- which account funds the purchase,
- whether sufficient balance exists,
- whether a hold exists for a contract,
- whether funds were released, refunded, or remain disputed,
- which gateway receipt funded the balance, when relevant.

### 5. Organization-bound purchase context

`story-006` explicitly uses `CasualFeeders` as the paying subject. The buyer-side
purchase contract therefore needs one frozen shape for acting on behalf of an
organization:

- operator participant
- organization subject
- payer account
- custody / authority reference

The host should own this context; `Arca` should consume it rather than inventing
it in middleware-local state.

### 6. Host capability surface for `Arca`

This is the most important planning artifact after the data shapes above.

The host should document a capability surface roughly like:

- `catalog.list_offers`
- `catalog.get_offer`
- `service_order.create`
- `service_order.submit`
- `procurement.execution.get`
- `procurement.execution.wait`
- `procurement.receipt.get`
- `ledger.account.get`
- `ledger.hold.get`
- `artifact_bundle.write_local`
- `notification.emit`

The exact transport is an implementation detail. The important point is semantic:
`Arca` talks to host-owned capabilities, not directly to transport-facing protocol
artifacts.

## Buyer-Node Components Required For Hard MVP

### 1. Service-catalog read model

The buyer Node needs a local read model of active standing offers.

Responsibilities:

- ingest or observe `service-offer.v1`,
- keep only active offers under `seq` and `ttl`,
- filter by service type, currency, queue posture, and bounded constraints,
- expose detail lookup by `offer/id`.

Why it matters:

- `Arca` cannot orchestrate purchases without a host-owned catalog surface.

Current status:

- closed in Node hard-MVP as a committed local catalog with
  `service-offer.v1` import, active-offer lookup, list/detail reads, and
  supervised module publication
- remaining gap beyond hard-MVP is remote observed-offer ingest and federated
  catalog distribution semantics

### 2. Buyer-side service-order ingress

The buyer Node needs a dedicated write surface for one purchase intent.

Responsibilities:

- validate `service-order.v1`,
- attach buyer context and workflow context,
- reject policy-illegal or economically impossible orders early,
- hand the result to the procurement bridge.

Why it matters:

- this is the legal buyer-side entry point that keeps `Arca` from mutating generic
  protocol payloads directly.

Current status:

- closed in Node hard-MVP through `service-order.v1` validation, classified
  bridge results, and thin local control plus launcher submit surfaces

### 3. Standing-offer to procurement bridge

The buyer Node needs a host-owned bridge that reuses the existing procurement
execution core while accepting a standing-offer based purchase model.

Responsibilities:

- open one selected-responder execution from a validated service order,
- bind the chosen provider and offer explicitly,
- project service parameters into the current procurement substrate,
- preserve workflow lineage and buyer references,
- keep the current contract and receipt path reusable.

Why it matters:

- current Node procurement works, but story-006 is service-catalog driven rather
  than offer-collection driven at purchase time.

Current status:

- closed in Node hard-MVP: one standing offer is resolved from the active
  catalog, buyer and organization context is attached host-side, settlement
  reservation happens inside the write gate, and procurement is opened through
  the existing selected-responder core
- remaining gap beyond hard-MVP is broader marketplace federation; richer
  operator views over policy-bound rejections are already closed in launcher and
  node-ui

### 4. Buyer-side settlement consumption surface

The buyer Node needs stable read-side settlement visibility even if the gateway
and escrow services are hosted elsewhere.

Responsibilities:

- resolve payer account,
- perform balance precheck,
- bind hold state to the running execution,
- expose release, refund, dispute, and review-required outcomes,
- surface gateway and escrow policy context to operator inspection.

Why it matters:

- `Arca` must be able to stop a workflow when funds are unavailable or when a
  remote paid phase remains unresolved.

Current status:

- closed in Node hard-MVP for deployment-local settlement:
  account and hold reads, idempotent gateway-receipt ingestion, hold
  create/void/release/refund/freeze, policy freezing, and dispute resolution are
  all runtime-backed
- gateway adapter MVP is now closed in Node hard-MVP through async gateway sync,
  append-only gateway facts, and control plus inspection surfaces
- remaining gap beyond hard-MVP is any later remote escrow boundary

### 5. Organization-subject consumption and acting-on-behalf-of resolution

The buyer Node needs an explicit host-side subject-resolution layer for:

- `participant:did:key`
- `org:did:key`
- payer account ownership
- custodian linkage

Responsibilities:

- resolve whether the buyer acts personally or on behalf of an organization,
- bind the purchase to the proper payer subject,
- keep the accountable actor visible in trace and receipts,
- prevent middleware from silently changing payer semantics.

Why it matters:

- `CasualFeeders` is central to `story-006`; this is not optional decoration.

Current status:

- closed in Node hard-MVP through host-side custodian resolution and
  organization-bound payer context during `service-order` bridge validation
- remaining gap beyond hard-MVP is richer organization storage and delegation
  policy beyond the current local custodian map

### 6. `Arca` host capability adapter

The buyer Node needs one explicit capability adapter or equivalent host API layer
through which `Arca` performs orchestration.

Responsibilities:

- expose catalog reads,
- expose service-order submission,
- expose execution and receipt inspection,
- expose local file output and notification actions,
- keep capability calls separate from raw protocol artifact authorship.

Why it matters:

- this is the core mechanism that makes `Arca` useful without making it a protocol
  loophole.

Current status:

- closed in Node hard-MVP: `Arca` now reuses existing `/v1/` catalog,
  execution, receipt, and settlement reads through one module auth token and
  also consumes host-owned workflow, notification, and artifact capabilities

### 7. Workflow-run state and local output staging

The buyer Node needs workflow-host surfaces that are local rather than wire-level.

Responsibilities:

- keep workflow run state,
- record phase boundaries and retries,
- join local workflow runs with remote procurement executions,
- write local output bundles for downstream systems such as WordPress import,
- emit bounded notifications.

Why it matters:

- Phase 4 in `story-006` is local packaging, not swarm procurement.

Current status:

- closed in Node hard-MVP: daemon persists workflow runs and step state, `Arca`
  orchestrates through host-owned workflow capabilities, notifications are
  persisted, and local artifacts are written and read through host-owned module
  roots
- product-level operator UX over workflow runs is now closed in launcher and
  node-ui hard-MVP
- remaining gap beyond hard-MVP is broader scheduling plus fan-out/fan-in policy

## Current Node Coverage vs Buyer Needs

The current Node workspace already provides useful foundations:

- supervised `http_local_json` middleware runtime,
- `middleware-init` and module reporting,
- selected-responder procurement core,
- committed procurement contracts and receipts,
- timeout cascade and review-required states,
- execution and receipt inspection,
- settlement-policy disclosure gating,
- stable `node-id` and `participant-id`.

The buyer-side gaps for `story-006` are therefore no longer in the core purchase
path. They now sit mostly above the current hard-MVP slice:

- remote or federated offer ingest beyond the local committed catalog,
- broader organization delegation and storage semantics beyond the current local
  custodian map,
- broader workflow planning than the currently implemented local multi-step
  orchestration, especially fan-out/fan-in policy,
- any later remote gateway or escrow boundary.

## Recommended Implementation Order

The original implementation order above is now largely complete in Node hard-MVP.
The next practical order for story-006 is:

### Phase E: hard-MVP product closure

Status in current workspace: closed.

Delivered:

1. gateway adapter MVP with async sync and append-only gateway facts,
2. richer operator views for module registry, workflow runs, and settlement plus
   participant restrictions,
3. explicit execution-to-receipt joins in launcher and node-ui.

### Phase F: marketplace beyond one local deployment

Implement:

1. remote observed-offer ingest and marketplace distribution semantics,
2. service-catalog topology beyond the local committed catalog, including a
   middleware-owned observed catalog path,
3. any later remote gateway or escrow boundary.

## Hard-MVP Boundary

The following are not required before the buyer-side `Arca` path becomes useful:

- full collaborative answer-room metadata projector,
- rich distributed search over all federations,
- final reputation marketplace layer,
- generalized workflow DSL standardization,
- full settlement-capable Node profile on the buyer side.

The hard-MVP buyer Node needs only enough host authority to:

- discover offers,
- place bounded orders,
- route them through procurement,
- observe settlement outcomes,
- and complete local packaging steps under host trace and policy.
