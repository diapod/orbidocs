# Supervised Prepaid Gateway and Escrow MVP

Based on:
- `doc/project/30-stories/story-001.md`
- `doc/project/30-stories/story-004.md`
- `doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`
- `doc/project/60-solutions/node.md`
- `doc/normative/30-core-values/en/CORE-VALUES.en.md`
- `doc/normative/50-constitutional-ops/en/SWARM-ECONOMY-SUFFICIENCY.en.md`
- `doc/normative/50-constitutional-ops/en/UNIVERSAL-BASIC-COMPUTE.en.md`

## Status

Proposed (Draft)

## Date

2026-03-28

## Executive Summary

Orbiplex already has a procurement lifecycle with explicit offers, contracts, and
receipts, but it still lacks a concrete MVP payment rail for priced work between
participants.

The decision of this proposal is:

1. paid task execution in MVP should run on a supervised federation-local prepaid
   ledger rather than on smart contracts or a crypto-native public rail,
2. economic balances must remain separate from reputation and procedural power,
3. the settlement path should use explicit escrow holds, dispute windows, and
   auditable gateway receipts for fiat-to-credit conversion,
4. the protocol core should continue to stay rail-neutral, while the first concrete
   MVP rail is `host-ledger`.

This keeps the system aligned with the current values corpus:

- reputation remains a safety and routing instrument rather than money,
- economic reward remains auditable but barred from procedural power,
- and the first useful marketplace flow can ship without forcing Orbiplex into a
  crypto-asset or smart-contract-first posture.

## Context and Problem Statement

The current corpus already covers:

- priced responder offers,
- procurement contracts,
- procurement receipts,
- `host-ledger` as an admissible settlement rail,
- a warning that protocol-external payment execution is outside the current Node core,
- the barrier against converting economic reward into procedural power.

What remains underspecified is the first concrete payment model that lets:

- user `A` hold a prepaid balance,
- reserve funds for an accepted offer from node `G`,
- keep the funds blocked while work is delivered,
- release or refund those funds deterministically,
- and account for fiat ingress and egress through trusted gateway nodes.

Without that model:

- `payment/amount` and `payment/currency` stay nominal rather than operational,
- escrow behavior becomes implementation folklore,
- double-spend and timeout behavior remain ambiguous,
- and the bridge between fiat and internal settlement units remains unaudited.

## Goals

- Define the first concrete MVP rail for paid procurement.
- Preserve the current procurement artifacts rather than replacing them.
- Keep economic accounting separate from reputation accrual.
- Support both `full-node` / `hybrid` and later `pod-client` participation.
- Make fiat entry and exit auditable through explicit gateway artifacts.
- Keep the trusted operational core small enough for one federation to run today.

## Non-Goals

- This proposal does not define a decentralized smart-contract rail.
- This proposal does not define cross-federation settlement portability.
- This proposal does not define a final legal or tax compliance model for each
  jurisdiction.
- This proposal does not yet freeze organization-subject identity semantics such as
  `org:did:key:...`; that should be handled in a later identity-focused proposal.
- This proposal does not make `UBC` spendable for market procurement.

## Decision

Orbiplex should adopt the following MVP settlement model for priced task execution:

1. a federation runs one authoritative supervised settlement ledger for MVP,
2. users and responders transact in a federation-defined internal unit, with the
   reference MVP symbol `ORC` ("Orbiplex Credit"),
3. prepaid balances are funded and redeemed only through trusted gateway nodes,
4. contract execution reserves funds through an explicit escrow hold,
5. settlement uses a dispute window and timeout cascade rather than immediate release,
6. reputation updates remain optional and separate, emitted through
   `reputation-signal.v1` from settlement facts rather than embedded into them.

## Proposed Actors

- `payer`: the asking participant or hosted user whose balance funds the work.
- `payee`: the responding participant that receives settlement for successful
  delivery.
- `gateway node`: a trusted node that converts external money into internal credits
  and optionally back out again.
- `escrow supervisor node`: a trusted node that manages holds, releases, refunds, and
  dispute transitions.
- `arbiter`: an optional actor that resolves disputed or high-stakes settlement.

For MVP, `gateway node` and `escrow supervisor node` MAY be the same operational
service or the same umbrella-organization node class.

## Core Model

### 1. Economic Unit

The protocol-visible procurement unit remains an internal settlement symbol, not a
fiat currency.

Reference MVP symbol:

- `ORC`

The protocol should treat `payment/currency = ORC` as the only unit it needs to
understand. Fiat pricing, spreads, and exchange policies remain gateway-local and are
audited through gateway artifacts rather than pushed into the procurement core.

### 2. Account Ownership

The settlement ledger should attach balances to accountable participation subjects,
not to raw infrastructure routing ids.

For MVP, the primary ownership shapes are:

- `participant-id`
- `pod-user-id` when a hosted-user flow is involved

The ledger should not treat `node-id` as the economic owner by default, because
`node-id` is the routing and hosting role, not necessarily the spending subject.

### 3. Ledger as Facts, Not Hidden Mutable State

The settlement subsystem should expose:

- an account artifact naming the account and its owner,
- a hold artifact naming reserved funds,
- transfer artifacts naming actual internal movements,
- gateway receipts naming fiat ingress or egress.

The balance itself is therefore a read model derived from append-only facts rather
than the sole source of truth.

## New MVP Artifact Family

The recommended new artifact family is:

1. `ledger-account.v1`
2. `ledger-hold.v1`
3. `ledger-transfer.v1`
4. `gateway-receipt.v1`

### 1. `ledger-account.v1`

Purpose:

- identify the settlement account,
- bind it to a participant or hosted-user owner,
- declare ledger scope, unit, and status.

Semantic minimum:

- `account/id`
- `owner/kind`
- `owner/id`
- `federation/id`
- `unit`
- `status`
- `created-at`

### 2. `ledger-hold.v1`

Purpose:

- reserve funds before work begins,
- define dispute and timeout semantics,
- provide the anchor for release or refund decisions.

Semantic minimum:

- `hold/id`
- `account/id`
- `contract/id`
- `amount`
- `unit`
- `status`
- `created-at`
- `work-by`
- `accept-by`
- `dispute-by`
- `auto-release-after`

Recommended MVP states:

- `active`
- `disputed`
- `released`
- `partially-released`
- `refunded`
- `expired`

### 3. `ledger-transfer.v1`

Purpose:

- record actual internal movement of value,
- bind the movement to a hold, gateway event, or administrative correction,
- distinguish release, refund, and other transfer classes.

Semantic minimum:

- `transfer/id`
- `kind`
- `from/account-id`
- `to/account-id`
- `amount`
- `unit`
- `created-at`
- optional `hold/id`
- optional `contract/id`
- optional `gateway-receipt/id`

The MVP transfer kind set should reserve at least:

- `top-up-credit`
- `escrow-hold`
- `release`
- `partial-release`
- `refund`
- `payout-debit`
- `adjustment`

### 4. `gateway-receipt.v1`

Purpose:

- audit the crossing between external money and internal credits,
- record which gateway node performed that crossing,
- preserve the rate or policy reference used by the gateway.

Semantic minimum:

- `receipt/id`
- `gateway/node-id`
- `direction` (`inbound` or `outbound`)
- `external/amount`
- `external/currency`
- `internal/amount`
- `internal/currency`
- `account/id`
- `ts`
- `external/payment-ref`
- optional `exchange-policy/ref`

## Extensions to Existing Procurement Artifacts

### `procurement-contract.v1`

The current contract artifact should remain the business contract boundary, but it
should gain explicit settlement bindings:

- `payer/account-ref`
- `payee/account-ref`
- `escrow/node-id`
- `escrow/hold-ref`
- `deadlines/work-by`
- `deadlines/accept-by`
- `deadlines/dispute-by`
- `deadlines/auto-release`

The current single `deadline-at` is too coarse for a hold-based procurement flow.

`payer/account-ref` and `payee/account-ref` should be canonical role-prefixed
settlement subject references such as:

- `participant:did:key:...`
- `org:did:key:...`

The role is already carried by the identifier prefix, so dedicated
`payer/kind` or `payee/kind` fields would only duplicate information and create
drift risk.

### `procurement-receipt.v1`

The current receipt should remain the auditable procurement outcome, but it should be
able to point clearly at settlement facts:

- `settlement/ref` should resolve to the release/refund outcome in the supervised
  ledger or a gateway-side payout record,
- `outcome` should remain contract-terminal rather than being overloaded with all
  escrow-state detail.

## MVP Lifecycle

The recommended happy path is:

1. the payer tops up `ORC` through a gateway node,
2. the gateway emits `gateway-receipt.v1`,
3. the supervised ledger records account credit,
4. the payer selects an offer,
5. settlement precheck confirms sufficient available balance,
6. the escrow supervisor creates `ledger-hold.v1`,
7. `procurement-contract.v1` binds to that hold,
8. the responder delivers the work,
9. the acceptance window opens,
10. one of three things happens:
    - payer confirms -> release,
    - payer opens dispute -> arbiter review,
    - payer is silent until timeout -> auto-release,
11. the ledger records release or refund through `ledger-transfer.v1`,
12. `procurement-receipt.v1` records the terminal contract outcome.

## Dispute Window and Timeout Cascade

MVP should explicitly support the following operational sequence:

`hold -> delivered -> acceptance window -> release/refund`

with a dispute branch:

`hold -> delivered -> dispute -> arbiter review -> release/refund`

The timeout cascade should be explicit and contract-bound:

- `work-by`: responder delivery deadline,
- `accept-by`: payer acceptance deadline,
- `dispute-by`: last moment for opening a formal dispute,
- `auto-release`: moment when escrow resolves automatically if the required prior
  conditions are met and no dispute is open.

This avoids deadlocks and griefing through indefinite fund blocking.

## Partial Release Reservation

MVP should reserve the data shape for partial release even if the first shipped UI
supports only simple cases.

Reason:

- real delivery can be partial,
- later introduction of partial settlement is expensive if the hold and transfer
  family assumes only binary outcomes,
- and arbiters otherwise need ad hoc manual bookkeeping that should belong in the
  ledger model.

## Single-Ledger Assumption

The explicit MVP assumption is:

> One federation uses one authoritative supervised settlement ledger for prepaid
> balances, holds, and internal transfers.

This means:

- double-spend prevention is achieved through ordinary serializable ledger
  operations,
- not through distributed consensus among many equal supervisors,
- and federation-scale multi-supervisor split-brain handling is deferred to
  post-MVP work.

## Separation from Reputation

Settlement facts and reputation facts should remain distinct artifacts.

Allowed pattern:

- a successful or disputed settlement MAY cause a separate `reputation-signal.v1`,
- that signal SHOULD reference the underlying `procurement-receipt` or dispute
  artifact through `basis/refs`,
- and consumers remain free to ignore, weight, or validate such signals under local
  policy.

Disallowed pattern:

- deriving governance weight directly from economic balance,
- collapsing a settlement receipt into a reputational verdict,
- or making credits a shortcut to procedural power.

## Relation to `UBC`

`UBC` remains a protective floor of participation and care. It must not become the
general spendable balance used to buy market work.

The settlement rail defined here is therefore:

- separate from `UBC`,
- separate from `creator credits`,
- and suitable for priced procurement rather than constitutional protection floors.

## Trade-offs

1. Supervised ledger vs smart contracts:
   - Benefit: practical MVP, simpler reversals, clearer operator accountability.
   - Cost: less decentralization and more trust in umbrella-operated nodes.
2. Rail-neutral protocol core vs one concrete MVP rail:
   - Benefit: keeps the core portable while still letting product scope move.
   - Cost: some semantic duplication between generic procurement and rail-specific
     settlement artifacts.
3. Separate gateway and escrow artifacts vs one overloaded receipt:
   - Benefit: better auditability and cleaner role boundaries.
   - Cost: more schema surface and more joins in tooling.
4. Single authoritative ledger vs multi-supervisor federation:
   - Benefit: simpler atomicity and faster MVP delivery.
   - Cost: federation-scale resilience is deferred.

## Open Questions

1. Should payout to external money be permitted from day one, or only top-up into
   the system with later payout enabled after compliance review?
2. Should the first MVP permit zero-fee gateway conversion, or should gateway fees be
   modeled from the beginning?
3. Should `ledger-account.v1` reserve `owner/kind = org` now, or should that wait for
   the organization-identity proposal?
4. What is the smallest acceptable arbiter policy for disputes under `host-ledger`
   settlement?

## Next Actions

1. Define `ledger-account.v1`, `ledger-hold.v1`, `ledger-transfer.v1`, and
   `gateway-receipt.v1`.
2. Extend `procurement-contract.v1` with escrow bindings and timeout cascade fields.
3. Extend `procurement-receipt.v1` so settlement joins remain explicit without
   overloading the receipt itself.
4. Write concrete engineering requirements for the supervised settlement MVP.
5. Later, open a separate identity workstream for organization subjects and
   `org:did:key:...`.
