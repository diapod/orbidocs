# Service Order to Procurement Bridge

Based on:
- `doc/project/30-stories/story-006.md`
- `doc/project/30-stories/story-006-buyer-node-components.md`
- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`
- `doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`
- `doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`
- `doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`
- `doc/project/50-requirements/requirements-011.md`

Date: `2026-03-30`
Status: Accepted hard-MVP bridge note

## Purpose

This memo records the host-owned mapping from `service-order.v1` into the current
procurement substrate.

It exists to keep one boundary explicit:

- `Arca` may author workflow intent and invoke host capabilities,
- the Node host remains the authority that derives and commits procurement-facing
  execution state.

## Layer Boundary

### Marketplace layer

Buyer-facing and provider-facing artifacts:

- `service-offer.v1`
- `service-order.v1`

### Procurement layer

Current executable core:

- `question-envelope.v1`
- `procurement-offer.v1`
- `procurement-contract.v1`
- `response-envelope.v1`
- `procurement-receipt.v1`

The bridge moves from the first layer into the second. It should not erase the
difference between them.

## Host-Owned Mapping

### Input

Validated `service-order.v1` plus the currently active `service-offer.v1` that it
references.

Catalog resolution is an explicit prerequisite. The host does not accept
pass-through standing offers from middleware in place of catalog resolution.

### Output

A host-owned procurement execution carrying:

- buyer subject context,
- payer context,
- chosen provider context,
- derived pricing and delivery constraints,
- workflow lineage refs,
- the normal settlement-aware procurement path.

## Bridge Steps

1. Resolve active offer

The host resolves `offer/id` against the active catalog read model and verifies:

- offer is active,
- order `offer/seq` still matches the latest active standing-offer sequence,
- provider references match,
- service type matches,
- order constraints stay within offer bounds.

2. Resolve buyer subject and payer context

The host resolves:

- buyer subject kind and id,
- acting-on-behalf-of organization context when relevant,
- payer account,
- operator participant reference when relevant.

For hard MVP, organization-bound buying is frozen as:

- accountable subject = `org:did:key:...`,
- operational signer = acting custodian `participant:did:key:...`,
- host verification = resolve `org/custodian-ref` and check that the operator
  participant is authorized to place the order.

3. Open buyer-local execution

The host opens one selected-responder execution scoped to the purchase.

The execution should preserve explicit refs to:

- `service-order/order-id`
- `service-offer/offer-id`
- `service-offer/offer-seq`
- workflow run and phase when present

For hard MVP those refs are preserved in buyer-local execution state and
buyer-local receipt annotations rather than being pushed into the procurement
wire contract.

4. Derive procurement-facing responder surface

For hard MVP, the host should derive one procurement-facing responder offer from
the standing service offer rather than forcing providers to emit a second explicit
offer artifact for the same purchase.

That derived responder surface is:

- host-authored,
- trace-visible,
- not middleware-authored,
- not an authority shift away from the provider's standing offer.

5. Run existing settlement-aware procurement path

After derivation, the host runs the current procurement substrate:

- funding precheck,
- settlement gating,
- contract creation,
- response intake,
- receipt and review-required handling.

For hard MVP, this step assumes one deployment-local settlement authority
boundary. Combined `gateway + escrow + catalog` deployment is acceptable. The
bridge therefore does not yet freeze a final remote buyer-to-escrow wire API for
hold creation or hold status lookup.

## Bridge Result Shape

The host-owned bridge returns one classified result to `Arca`:

- `opened-execution`
- `rejected`

When rejected, the result carries one machine-readable classifier such as:

- `queue-saturated`
- `offer-not-found`
- `offer-expired`
- `offer-seq-mismatch`
- `service-type-mismatch`
- `provider-mismatch`
- `price-exceeded`
- `currency-mismatch`
- `custodian-mismatch`
- `settlement-blocked`
- `other-reason`

Optional `rejected-reason` may accompany any classifier and should remain
human-readable with hard-MVP maximum size `1024` characters.

## Mapping Guidance

### `service-offer.v1` -> derived procurement-facing data

Recommended mapping:

- provider identity -> responder identity
- pricing -> responder price proposal
- delivery bound -> contract deadline seed
- queue posture -> admission decision before contract creation
- hybrid / model-first -> policy and operator-visible annotations
- constraints/output -> answer bounds or format expectations when possible

### `service-order.v1` -> procurement execution input

Recommended mapping:

- buyer context -> payer / requester side execution context
- request input -> question/request body or execution input payload
- max price -> procurement price ceiling
- requested delivery bound -> stricter deadline if admissible
- workflow lineage -> execution annotations and trace refs

When queue posture rejects the order, the host records an exchange-level or
order-level rejection such as `queue-saturated` and stops before procurement
contract creation.

## What `Arca` May and May Not Do

### `Arca` may

- select one offer from host-visible catalog data,
- create one service-order intent,
- submit that order through a host capability,
- wait on host execution states,
- react to receipt or failure outcomes,
- shape local workflow payloads within host policy.

### `Arca` must not

- fabricate the derived procurement-facing responder surface,
- rewrite payer identity after host resolution,
- emit `procurement-contract.v1` directly,
- emit `procurement-receipt.v1` directly,
- bypass settlement gating or hold state.

## Operator Visibility

The bridge should remain operator-visible through:

- execution inspection,
- trace refs to `service-order` and `service-offer`,
- settlement and receipt joins,
- explicit buyer subject and payer resolution.

This keeps the bridge diagnosable instead of turning it into middleware folklore.
