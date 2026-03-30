# Requirements 012: Service Offers, Service Orders, and Buyer-Side Procurement Bridge

Based on:
- `doc/project/30-stories/story-006.md`
- `doc/project/30-stories/story-006-buyer-node-components.md`
- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`
- `doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`
- `doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`
- `doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`
- `doc/project/50-requirements/requirements-010.md`
- `doc/project/50-requirements/requirements-011.md`
- `doc/project/60-solutions/node.md`

Date: `2026-03-30`
Status: Draft (hard MVP slice)

## Executive Summary

This document defines the minimum buyer/provider marketplace contract layer needed
for the hard-MVP path of `story-006`.

The core decision is:

- provider-side standing offers should use `service-offer.v1`,
- buyer-side purchase intent should use `service-order.v1`,
- the Node host should own the bridge from `service-order` into the current
  procurement substrate,
- middleware such as `Arca` and `Dator` must consume those host-owned contracts
  rather than inventing equivalent lower-layer payloads directly.

## Context and Problem Statement

The current Node execution substrate already supports procurement contracts and
receipts, but story-006 is catalog-driven and standing-offer driven.

Without a dedicated marketplace contract layer:

- standing offers remain plugin-local,
- buyer-side ordering remains implicit,
- `Arca` is tempted to overreach into procurement payload authorship,
- Node loses a clear boundary between workflow orchestration and protocol truth.

## Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-001 | The system MUST define `service-offer.v1` as the standing exchange-facing artifact for one published priced service offer. | Fact | Proposal 021 |
| FR-002 | `service-offer.v1` MUST remain distinct from `node-advertisement.v1` and `capability-advertisement.v1`. | Fact | Proposal 021 |
| FR-003 | `service-offer.v1` MUST carry enough provider-visible data to support catalog listing and buyer selection: provider identity, service type, price, delivery bound, queue posture, and offer freshness. | Fact | Story 006 + Proposal 021 |
| FR-004 | `service-offer.v1` MUST be signed by the provider-side accountable subject rather than by transport-only node identity. | Fact | Story 006 + Proposal 021 |
| FR-005 | The system MUST define `service-order.v1` as the buyer-facing purchase-intent artifact referencing one standing offer. | Fact | Proposal 021 |
| FR-006 | `service-order.v1` MUST carry buyer subject context sufficient for participant-scoped and organization-scoped purchases. | Fact | Story 006 + Proposal 017 |
| FR-007 | `service-order.v1` MUST carry bounded request input, unit count, and max-price semantics before procurement execution begins. | Fact | Proposal 021 |
| FR-007a | When `pricing/currency = ORC`, both `service-offer.v1.pricing/amount` and `service-order.v1.pricing/max-amount` MUST carry ORC minor units with fixed decimal scale `2`. | Fact | Proposal 021 + Requirements 007 |
| FR-008 | `service-order.v1` MUST be signed by the buyer-side accountable subject. | Fact | Proposal 021 |
| FR-009 | The Node host MUST validate `service-order.v1` against the referenced active `service-offer.v1` before opening procurement execution. | Fact | Proposal 021 |
| FR-010 | The Node host MUST own the bridge from `service-order.v1` into the current procurement lifecycle; middleware MUST NOT fabricate the lower-layer procurement artifacts directly. | Fact | Proposal 021 + project values |
| FR-011 | The first hard-MVP bridge MUST reuse the current selected-responder procurement substrate instead of inventing a separate economic closure family. | Fact | Proposal 021 |
| FR-012 | The buyer-side hard MVP MUST expose a host-owned catalog read surface over active `service-offer.v1` artifacts. | Fact | Story 006 buyer note |
| FR-013 | The buyer-side hard MVP MUST expose a host-owned write surface for validated service-order ingress. | Fact | Story 006 buyer note |
| FR-014 | Buyer-side service-order execution MUST resolve payer context before settlement-aware procurement begins. | Fact | Proposal 016 + Proposal 017 |
| FR-015 | `Arca` MUST route remote paid workflow steps through `service-order` and the host-owned bridge, rather than through side-channel vendor or transport payload creation. | Fact | Requirements 011 + Proposal 021 |
| FR-016 | The system SHOULD preserve workflow lineage in `service-order.v1` so a buyer-side workflow can trace a purchase back to run and phase context. | Inference | Story 006 |
| FR-017 | The buyer-side hard MVP SHOULD expose enough read-side settlement state to let `Arca` stop on insufficient funds, unresolved holds, or review-required outcomes. | Inference | Story 006 + Proposal 016 |

## Non-Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| NFR-001 | Marketplace-layer artifacts MUST remain smaller and semantically clearer than the underlying procurement and settlement substrate they project into. | Fact | Contract-first architecture |
| NFR-002 | `service-offer.v1` and `service-order.v1` MUST be versioned schemas with examples and generated schema docs before buyer-side implementation begins. | Fact | User intent + project values |
| NFR-003 | The host-owned bridge MUST keep workflow intent separate from procurement authority so diagnostics can attribute failures to the correct layer. | Fact | Project values |
| NFR-004 | Catalog, order ingress, and procurement bridge SHOULD remain host-owned surfaces visible to operators rather than opaque middleware side effects. | Inference | Operability |
| NFR-005 | Middleware convenience MUST NOT collapse the authority boundary between workflow orchestration and economic contract formation. | Fact | Requirements 011 + project values |

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| A service order references an expired or superseded offer | Buyer thinks a purchase is valid when it is not | Validate against active catalog state under `sequence/no` and `expires-at` before opening execution. |
| `Arca` tries to bypass host procurement by emitting lower-layer payloads directly | Hidden economic side channel | Keep service-order ingress and bridge host-owned; reject direct lower-layer authorship by middleware. |
| Organization-bound purchase context is ambiguous | Wrong payer or wrong audit trail | Require explicit buyer subject context and host-owned payer resolution. |
| Offer and order price semantics drift | Contract surprises or accidental overspend | Require `pricing/max-amount` on order and match it against active offer terms. |
| Catalog remains plugin-local | Buyers cannot inspect or debug offer selection | Require host-visible catalog read surfaces. |

## Open Questions

1. Should hard MVP require one explicit `withdrawn` state for standing offers, or is expiry plus replacement enough?
2. Should `service-order.v1` carry one explicit preferred confirmation mode, or should that remain advisory only?
3. How much of the derived procurement-facing bridge state should become operator-visible read-model data?

## Next Actions

1. Add canonical JSON Schema files for `service-offer.v1` and `service-order.v1`.
2. Add example payloads for both artifacts.
3. Record the bridge mapping in a dedicated project note.
4. Use those artifacts as the prerequisite boundary for buyer-side Node implementation planning.
