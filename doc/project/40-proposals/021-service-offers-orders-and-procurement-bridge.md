# Proposal 021: Service Offers, Service Orders, and the Host-Owned Procurement Bridge

Based on:
- `doc/project/30-stories/story-006-voluntary-swarm-exchange.md`
- `doc/project/30-stories/story-006-buyer-node-components.md`
- `doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`
- `doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`
- `doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`
- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/40-proposals/020-bundled-python-middleware-modules.md`
- `doc/project/50-requirements/requirements-010-middleware-executor.md`
- `doc/project/50-requirements/requirements-011-dator-arca-contracts.md`
- `doc/project/60-solutions/000-node/000-node.md`
- `doc/normative/50-constitutional-ops/en/MARKETPLACE-ANTI-FRAUD-POLICY.en.md`

Extended by:

- `doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`

## Status

Accepted (hard MVP contract)

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
- Keep marketplace influence gated by value caps, escrow/procurement contracts,
  settled receipts, and anti-fraud limits for newcomers or low-evidence
  participants.

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
   - signed operationally by the provider-side participant subject,
   - catalog-visible and TTL-bounded.
2. `service-order.v1`
   - buyer-side purchase intent artifact,
   - signed operationally by the buyer-side participant subject,
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

### Anti-Fraud Surface Limits

Marketplace access is an influence surface.
The host-owned bridge SHOULD therefore consume the local entry profile and
capability-limit policy before converting a service order into procurement.

The hard-MVP baseline is:

- no unsolicited financial offers through DM,
- low value caps for new or low-evidence participants,
- escrow or procurement contracts for non-trivial risk,
- no transferable reputation from self-dealing or closed receipt loops,
- stronger IAL, procedural reputation, cooling-off, and dispute paths for
  high-value surfaces.

This keeps `service-offer` and `service-order` useful without turning the
catalog into an unbounded acquisition channel.

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
- `pricing/unit-kind`
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

### Extensible Inference Execution Posture

An offer that may be fulfilled through model or external-agent inference should
publish a provider-declared execution posture separately from the service type,
human-curation mode, and evidence criteria. The shared offer contract should
therefore gain a bounded namespaced characteristic extension governed by
Proposal 090 rather than another global closed repertoire of problem classes or
providers.

The separate `inference-execution-posture.v1` characteristic may state
`local-only`, `may-use-non-local`, `non-local-required`, or `unknown`, plus
optional open provider refs and their disclosure commitment/state/ref. It binds
the offer signer, exact offer generation or validity, assertion scope, and
versioned local-processing-boundary ref. It is a signed promise or routing hint
before selection, not proof of how one purchased result was actually produced.
The buyer or local operator owns admission, filtering, consent, and UI policy;
the provider does not acquire that authority through its disclosure
declaration. The delivered result must carry its own realized
`inference-execution-provenance.v1` value.

The existing Corpus `corpus/model-class` field remains a compatibility
projection for current V1 offers. It must not become the semantic source for
the new characteristic: its closed values conflate execution locality with
human curation and cannot represent operator- or community-defined provider
profiles without central schema churn.

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
- `offer/seq`
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

Hard-MVP freeze:

- `offer/id` is a prefixed URN, not a free string,
- `order/id` is a prefixed URN, not a free string,
- `buyer/subject-kind` is limited to `participant` and `org`,
- `buyer/operator-participant-id` is required when the buyer acts on behalf of an
  organization.

## Host-Owned Bridge Semantics

### Validation phase

Given one `service-order.v1`, the host must:

1. resolve the referenced active `service-offer.v1`,
2. verify that order `offer/seq` still matches the latest active standing-offer
   sequence,
3. verify that provider and offer references match,
4. verify that the offer is still active under `sequence/no` and `expires-at`,
5. verify that requested service parameters stay within the offer constraints,
6. verify that buyer-side max price and currency admit the current offer,
7. resolve buyer subject and payer context.

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

For hard MVP, marketplace lineage is preserved in buyer-local execution state and
buyer-local receipt annotations:

- `offer/id`,
- `offer/seq`,
- `order/id`.

Those refs should not be treated as provider-facing procurement wire fields.

### Remote provider closeout

Remote execution preserves the same host-owned boundary:

1. the buyer host validates the service order, creates the hold, and persists a
   request/correlation record before remote dispatch,
2. `Arca` sends the host-issued request through Artifact Delivery,
3. `Dator` returns one terminal `service-order.result.v1` through Artifact Delivery,
4. the host binds the exact AD invocation to a one-shot acceptor/schema/digest token,
   and the buyer-side Arca acceptor relays that opaque authority with the artifact,
5. the buyer host consumes the token, derives source identity from host-owned AD
   provenance, and validates provider identity, workflow lineage, correlation,
   schema, size, and digest before effects,
6. the buyer host alone projects success into acceptance/manual release or projects
   failure/rejection into refund plus terminal receipt,
7. `Arca` observes the authoritative execution snapshot and updates only its workflow
   projection; after `manual-review-only` release, resuming a paused workflow is a
   separate explicit orchestration transition.

An identical result digest is an idempotent replay. A different digest for an
already-admitted request/correlation is a conflict and MUST fail closed. Provider
`hold/ref`, `receipt/ref`, and `settlement/refs` values MUST NOT authorize settlement;
the buyer host uses its own durable joins. Module-relayed source/trust fields are not
authority. Result-admission failures expose a stable reason code and explicit
`retryable` datum; Arca must not classify them by matching error strings.

The paid three-node Story-009 acceptance exercises this path with buyer Arca on node
A and remote Dator providers on nodes B and C, including AD request/result transport,
manual release, explicit workflow resume, terminal receipt, and released hold.

### Zero-price confirmation fallback

When the selected standing offer has `pricing/amount = 0`, the host-owned
bridge should use a deterministic local fallback: **zero price path does not
require confirmation**. This avoids projecting a free, local execution into a
settlement confirmation policy that only matters once funds, holds, or escrow
are involved.

`confirmation/mode` remains the exchange/procurement wire field with the
official confirmation vocabulary. Local middleware or profile config may use a
convenience value such as `confirmation_mode: "automatic"` to request this
zero-price fallback, but that value must be normalized before publishing the
wire offer; it is not an official `confirmation/mode` value.

For hard MVP, queue saturation is modeled before procurement contract creation:

- a service order may be rejected with `queue-saturated`,
- this is an exchange-level or order-level admission outcome,
- it is not a transport or capability mismatch,
- it must not be normalized into a generic protocol error.

## Identity and Settlement Compatibility

The new marketplace artifacts should remain compatible with:

- participant-scoped buying,
- organization-scoped buying,
- the supervised prepaid ORC rail,
- buyer-side workflow orchestration through `Arca`,
- provider-side service publication through `Dator`.

In particular:

- a service offer is signed by the provider-side participant subject,
- a service order is signed by the buyer-side participant subject,
- when the accountable buyer subject is an organization, hard MVP uses the
  acting custodian participant as the operational signer together with explicit
  `buyer/subject-kind = org`, `buyer/subject-id`, and
  `buyer/operator-participant-id`,
- the host bridge is responsible for verifying custodian authority and attaching
  the correct settlement and payer context,
- the procurement contract and receipt remain the current economic closure points.

The custodian check should remain a distinct host capability with explicit error
semantics rather than an implicit helper hidden inside the bridge body.

When `pricing/currency = ORC`, both `pricing/amount` and `pricing/max-amount`
follow the fixed ORC scale-2 rule from the supervised settlement rail. The
marketplace layer therefore carries integer minor units on the wire, while
human-facing displays render them as `major.minor ORC`.

The bridge computes economic totals only from machine-readable fields:

- `pricing/unit-kind`,
- `pricing/amount`,
- `request/units`,
- `pricing/max-amount`.

Human-readable labels such as `pricing/unit` are descriptive only and must not be
parsed by the host to derive price, hold amount, or contract total.

For hard MVP, the bridge also freezes one deployment assumption:

- the settlement authority boundary is deployment-local,
- combined `gateway + escrow + catalog` deployment is acceptable,
- the buyer-side bridge does not yet standardize a final remote buyer-to-escrow
  hold API; remote provider execution and result closeout do not relax this boundary.

The same assumption applies to catalog and escrow runtime placement:

- catalog and escrow live in the daemon in hard MVP,
- gateway may remain a separate trusted local process reached through one host
  adapter surface.

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

No unresolved questions remain for this proposal slice. The decisions below
record the approved defaults.

Resolved 2026-07-05:

1. Provider-side standing-offer updates use `sequence/no` replacement and hard
   MVP also admits explicit withdrawal. Withdrawal must be an auditable action,
   not only an absence from the active projection.
2. `service-order.v1` carries an explicit settlement mode hint. The host may
   still validate the hint against the standing offer and policy.
3. The host exposes the derived procurement offer in a redacted operator trace.
   The trace must be sufficient for diagnostics without leaking secrets or
   internal-only policy material.
4. Hard MVP catalog search/filtering includes active offers by capability,
   provider, price/currency, and tags/topic.
5. Classified pre-procurement rejection outcomes exposed to `Arca` use a typed
   rejection class, reason code, and retryability flag, without raw host
   internals.
6. Inference execution posture is a separate extensible signed offer contract
   bound to its signer, subject, generation/scope, and exact processing-boundary
   ref; realized execution provenance belongs to the delivered result. Exact
   provider disclosure remains optional and open rather than a global enum, and
   the buyer or local operator retains admission and presentation policy.
7. Generic remote procurement carries realized provenance through a compatible
   `service-order.result` revision or immutable sidecar ref. It does not extend
   V1 in place: Dator binds the producer value, Artifact Delivery carries it
   opaquely, and buyer-side Arca verifies and preserves it without upgrading the
   producer's evidence or reinterpreting its boundary.

## Implementation State

The hard-MVP schemas, host-owned bridge, settlement hint validation, classified
rejections, redacted inspection surface, durable remote dispatch correlation, and
buyer-host AD result closeout are implemented. Remaining work belongs to broader
marketplace policy, remote escrow topology, and post-MVP catalog evolution rather
than to this bridge contract. The Proposal 090 offer-characteristic extension is
planned post-MVP work and does not change the current hard-MVP completion claim.

## Post-MVP Tracker

| ID | Work item | Status | Done criteria / evidence |
| :--- | :--- | :--- | :--- |
| `offer-inference-execution-posture` | Add the separate Proposal 090 provider-declared execution-posture contract to `service-offer` without closing provider or profile vocabularies. | `todo` | A compatible schema revision or successor carries `inference-execution-posture.v1` with assertion owner, exact offer subject/generation/scope, processing-boundary ref, optional open provider refs, provider disclosure commitment/state/ref, and signed offer provenance. Consumer policy remains buyer/operator-owned. Absence, expiry, invalid signature, missing boundary, and an unrelated boundary remain `unknown` or non-match; current `corpus/model-class` can be projected for compatibility but is not the source of truth. Positive and negative fixtures distinguish an offer promise from realized result provenance. |
| `procurement-inference-execution-provenance` | Carry realized inference provenance through the generic Dator → `service-order.result` → Artifact Delivery → Arca return path. | `todo` | A compatible result revision or immutable sidecar ref binds `inference-execution-provenance.v1` without extending V1 in place. Dator stamps or preserves the producer value, Artifact Delivery protects and carries it opaquely with its own source/digest evidence, and Arca verifies and preserves it while applying buyer policy. Fixtures reject missing, stripped, substituted, replay-conflicting, and unrelated-boundary metadata; no carrier infers locality from offer posture, transport, or provider name. |
