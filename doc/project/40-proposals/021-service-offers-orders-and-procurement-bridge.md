# Proposal 021: Service Offers, Service Orders, and the Host-Owned Procurement Bridge

Based on:
- `doc/project/30-stories/story-006.md`
- `doc/project/30-stories/story-006-buyer-node-components.md`
- `doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`
- `doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`
- `doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`
- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/40-proposals/020-bundled-python-middleware-modules.md`
- `doc/project/50-requirements/requirements-010.md`
- `doc/project/50-requirements/requirements-011.md`
- `doc/project/60-solutions/node.md`

## Status

Proposed (Draft)

## Date

2026-03-30

## Executive Summary

`story-006` introduces a marketplace-style service exchange that is not captured
fully by the current procurement core alone.

The key decision of this proposal is:

1. `service-offer.v1` should become a first-class exchange-facing standing-offer
   artifact,
2. `service-order.v1` should become the buyer-facing purchase intent artifact,
3. the currently executable Node substrate should still remain procurement-based,
4. therefore the first hard-MVP implementation should use a host-owned bridge from
   `service-order.v1` into the current procurement lifecycle rather than allowing
   middleware to fabricate arbitrary procurement payloads directly.

This keeps the trusted core small:

- marketplace semantics become explicit,
- Node remains the authority for signing, settlement, and procurement,
- `Arca` remains a hosted workflow module rather than a protocol loophole.

## Context and Problem Statement

The current Node workspace already has a usable procurement and settlement-aware
execution substrate:

- `procurement-offer.v1`
- `procurement-contract.v1`
- `procurement-receipt.v1`
- `response-envelope.v1`
- `ledger-hold.v1`
- `gateway-receipt.v1`

This is enough for selected-responder execution, but not yet for the buyer-side
marketplace shape in `story-006`, where:

- providers publish standing offers,
- buyers browse active offers in a catalog,
- a buyer picks a concrete offer before opening paid execution,
- `Arca` orchestrates repeated purchases on behalf of a buyer subject such as an
  organization.

Without explicit `service-offer` and `service-order` artifacts:

- catalog semantics remain plugin-local rather than protocol-visible,
- `Arca` is pressured to treat workflow state as authority to mutate lower-layer
  payloads,
- the host boundary between workflow intent and procurement execution becomes
  implicit.

## Goals

- Define the minimum hard-MVP artifact pair for the marketplace layer:
  `service-offer.v1` and `service-order.v1`.
- Keep the currently implemented procurement core reusable.
- Freeze one host-owned bridge from `service-order` into procurement so Node
  remains authoritative over lower-layer artifacts.
- Preserve organization-bound buying and settlement-aware execution.
- Keep `Dator` and `Arca` within the existing middleware envelope contract rather
  than adding a second execution protocol.

## Non-Goals

- This proposal does not replace the procurement family.
- This proposal does not define the full catalog transport topology.
- This proposal does not freeze a final `service-result.v1` family.
- This proposal does not define the full `Arca` workflow DSL.
- This proposal does not grant middleware direct authorship over settlement or
  procurement facts.

## Decision

Orbiplex should adopt the following hard-MVP layering:

1. `service-offer.v1`
   - standing exchange-facing publication artifact,
   - signed by the provider-side accountable subject,
   - catalog-visible and TTL-bounded.
2. `service-order.v1`
   - buyer-side purchase intent artifact,
   - signed by the buyer-side accountable subject,
   - references one standing offer and carries bounded purchase parameters.
3. `service-order -> procurement` host bridge
   - Node-owned transformation boundary,
   - validates the order against the selected active offer,
   - derives the procurement-facing execution state,
   - reuses the existing selected-responder execution substrate.

## Proposed Artifact Roles

### `service-offer.v1`

Purpose:

- publish one standing paid service offer,
- expose price, queue posture, delivery bound, and service constraints,
- make hybrid/human-in-the-loop semantics visible,
- let a catalog index active offers without becoming the authority over them.

This artifact belongs to the provider side. It is distinct from:

- `node-advertisement.v1`
- `capability-advertisement.v1`

Those remain transport- and capability-facing rather than market-facing.

### `service-order.v1`

Purpose:

- let a buyer place one explicit order against one standing offer,
- bind the purchase to a buyer subject and payer context,
- carry workflow lineage when the purchase comes from `Arca`,
- define bounded input, output, and price expectations before procurement begins.

This artifact belongs to the buyer side.

### Host-owned bridge

Purpose:

- keep middleware from fabricating arbitrary procurement artifacts,
- let the host resolve and validate one standing offer,
- project service exchange into the currently executable procurement core.

This bridge is not merely an implementation detail. It is the authority boundary
that preserves Node control over:

- procurement identity,
- settlement semantics,
- policy gating,
- traceability.

## Recommended Hard-MVP Shape of `service-offer.v1`

The minimum contract should include:

- `offer/id`
- `created-at`
- `published-at`
- `expires-at`
- `sequence/no`
- `provider/node-id`
- `provider/participant-id`
- `service/type`
- `service/description`
- `pricing/amount`
- `pricing/currency`
- `pricing/unit`
- `delivery/max-duration-sec`
- `queue/auto-accept`
- `queue/max-depth`
- optional `queue/current-depth`
- optional `constraints/input`
- optional `constraints/output`
- `hybrid`
- optional `model-first`
- optional `confirmation/mode`
- `signature`

## Recommended Hard-MVP Shape of `service-order.v1`

The minimum contract should include:

- `order/id`
- `created-at`
- `buyer/node-id`
- `buyer/subject-kind`
- `buyer/subject-id`
- optional `buyer/operator-participant-id`
- `provider/node-id`
- `provider/participant-id`
- `offer/id`
- `service/type`
- `request/units`
- `request/input`
- optional `request/output-constraints`
- `pricing/max-amount`
- `pricing/currency`
- optional `delivery/requested-by`
- optional `workflow/run-id`
- optional `workflow/phase-id`
- optional `lineage/upstream-refs`
- `signature`

## Host-Owned Bridge Semantics

### Validation phase

Given one `service-order.v1`, the host must:

1. resolve the referenced active `service-offer.v1`,
2. verify that provider and offer references match,
3. verify that the offer is still active under `sequence/no` and `expires-at`,
4. verify that requested service parameters stay within the offer constraints,
5. verify that buyer-side max price and currency admit the current offer,
6. resolve buyer subject and payer context.

If any of these fail, the order must stop before procurement execution begins.

### Projection phase

For hard MVP, the host should then:

1. open one buyer-local selected-responder execution,
2. derive one procurement-facing responder offer surface from the standing
   `service-offer.v1`,
3. bind the execution to the chosen provider and buyer context,
4. run the current funding and settlement precheck,
5. proceed into the existing `procurement-contract.v1` path.

The derived procurement-facing state is host-owned. `Arca` and `Dator` may shape
intent and metadata, but they are not the authority that authors the lower-layer
artifacts.

## Identity and Settlement Compatibility

The new marketplace artifacts should remain compatible with:

- participant-scoped buying,
- organization-scoped buying,
- the supervised prepaid ORC rail,
- buyer-side workflow orchestration through `Arca`,
- provider-side service publication through `Dator`.

In particular:

- a service offer is signed by the provider-side accountable subject,
- a service order is signed by the buyer-side accountable subject,
- the host bridge is responsible for attaching the correct settlement and payer
  context,
- the procurement contract and receipt remain the current economic closure points.

When `pricing/currency = ORC`, both `pricing/amount` and `pricing/max-amount`
follow the fixed ORC scale-2 rule from the supervised settlement rail. The
marketplace layer therefore carries integer minor units on the wire, while
human-facing displays render them as `major.minor ORC`.

## Trade-offs

### Benefits

- standing-offer marketplaces become explicit,
- the buyer-side purchase boundary becomes auditable,
- `Arca` remains bounded by host authority,
- current procurement runtime is reused rather than discarded.

### Costs

- one more artifact pair to version and validate,
- one more bridge layer to maintain,
- catalog/read-model work becomes part of the practical MVP path.

### Risks

- if the bridge is under-specified, implementation may drift into hidden
  middleware authority,
- if `service-order` becomes too expressive too early, it may duplicate
  procurement rather than feeding it,
- if provider and buyer subjects are not frozen clearly, settlement ambiguity will
  leak upward into workflows.

## Open Questions

1. Should provider-side standing-offer updates be represented only by
   `sequence/no` replacement, or should hard MVP also admit explicit withdrawal?
2. Should `service-order.v1` carry one explicit settlement mode hint, or should
   that remain fully host-derived from the standing offer plus policy?
3. Should the host expose the derived procurement offer in operator trace, or keep
   it implicit as an internal bridge product?
4. Which subset of catalog search and filtering is required for hard MVP, beyond
   simple active-offer listing?

## Next Actions

1. Freeze `service-offer.v1.schema.json`.
2. Freeze `service-order.v1.schema.json`.
3. Record the host-owned `service-order -> procurement` bridge as a dedicated note.
4. Add buyer-side requirements for catalog read, service-order ingress, and the
   bridge boundary.
5. Let Node implementation planning proceed only after those artifacts are
   reviewed.
