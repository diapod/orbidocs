# Requirements 007: Supervised Prepaid Gateway and Escrow MVP

Based on:
- `doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`
- `doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`
- `doc/project/30-stories/story-001.md`
- `doc/project/30-stories/story-004.md`
- `doc/normative/50-constitutional-ops/en/SWARM-ECONOMY-SUFFICIENCY.en.md`
- `doc/normative/50-constitutional-ops/en/UNIVERSAL-BASIC-COMPUTE.en.md`

Date: `2026-03-28`
Status: Draft (MVP scope)

## Executive Summary

This document defines the first concrete engineering requirements for paid
procurement in Orbiplex using a supervised federation-local prepaid ledger.

The MVP priorities are:

- explicit prepaid account ownership,
- escrow holds before work begins,
- dispute window plus timeout cascade,
- auditable fiat entry and exit through trusted gateways,
- and strict separation between economic balance and reputation.

## Context and Problem Statement

Procurement already has:

- offer artifacts,
- contract artifacts,
- receipt artifacts,
- and a rail-neutral contract model.

What it still lacks is a concrete settlement substrate that lets the system:

- check available balance before contract creation,
- reserve funds atomically,
- release or refund those funds predictably,
- and audit the bridge between external money and internal credits.

Without these requirements, `host-ledger` remains nominal rather than actionable.

## Proposed Model / Decision

### Actors and Boundaries

- `Payer`: participant or hosted user funding a paid task.
- `Payee`: participant receiving payment after successful delivery.
- `Gateway Node`: trusted node that turns external money into internal credits and
  optionally internal credits back into external money.
- `Escrow Supervisor`: trusted node that creates holds, resolves release/refund, and
  enforces timeout semantics.
- `Arbiter`: optional confirmer for disputed or high-stakes outcomes.

### Core Data Contracts (normative)

- `LedgerAccount`:
  - `account/id`, `owner/kind`, `owner/id`, `federation/id`, `unit`, `status`,
    `created-at`.
- `LedgerHold`:
  - `hold/id`, `account/id`, `contract/id`, `amount`, `unit`, `status`,
    `created-at`, `work-by`, `accept-by`, `dispute-by`, `auto-release-after`.
- `LedgerTransfer`:
  - `transfer/id`, `kind`, `from/account-id`, `to/account-id`, `amount`, `unit`,
    `created-at`, optional `hold/id`, optional `contract/id`,
    optional `gateway-receipt/id`.
- `GatewayReceipt`:
  - `receipt/id`, `gateway/node-id`, `direction`, `external/amount`,
    `external/currency`, `internal/amount`, `internal/currency`, `account/id`, `ts`,
    `external/payment-ref`, optional `exchange-policy/ref`.
- Extensions to `ProcurementContract`:
  - `payer/account-ref`, `payee/account-ref`, `escrow/node-id`,
    `escrow/hold-ref`, `deadlines/work-by`, `deadlines/accept-by`,
    `deadlines/dispute-by`, `deadlines/auto-release`.
- Extension to `ProcurementReceipt`:
  - explicit link from `settlement/ref` to final ledger outcome.

### Explicit MVP Assumption

Within one federation, MVP runs on one authoritative supervised settlement ledger.

This assumption is normative for MVP behavior of:

- available-balance checks,
- hold creation,
- release/refund,
- and double-spend prevention.

## Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-001 | The MVP settlement unit MUST be an internal ledger unit independent from fiat pricing; the reference symbol is `ORC`. | Fact | Proposal 016 |
| FR-002 | The system MUST keep economic balance and reputation as separate artifact families and MUST NOT derive governance weight from balance. | Fact | Proposal 016 |
| FR-003 | A federation operating paid procurement MUST run one authoritative supervised settlement ledger for MVP. | Fact | Proposal 016 |
| FR-004 | The system MUST support a `ledger-account` artifact that binds an account to an accountable owner and settlement unit. | Fact | Proposal 016 |
| FR-005 | `ledger-account` ownership MUST support at least `participant` and `pod-user` as owner kinds. | Fact | Story 004 + Proposal 016 |
| FR-006 | The system MUST perform an available-balance precheck before creating a paid procurement contract. | Fact | Requirements 001 FR-015 + Proposal 016 |
| FR-007 | When balance is sufficient, the escrow supervisor MUST create a `ledger-hold` before remote paid execution begins. | Fact | Proposal 016 |
| FR-008 | `ledger-hold` MUST include explicit status and timeout fields for work, acceptance, dispute, and auto-release. | Fact | Proposal 016 |
| FR-009 | `ledger-hold.status` MUST support at least `active`, `disputed`, `released`, `partially-released`, `refunded`, and `expired`. | Fact | Proposal 016 |
| FR-010 | `procurement-contract.v1` MUST gain explicit settlement bindings: `payer/account-ref`, `payee/account-ref`, `escrow/node-id`, and `escrow/hold-ref`. | Fact | Proposal 016 |
| FR-011 | `procurement-contract.v1` MUST carry a timeout cascade rather than only one coarse responder deadline. | Fact | Proposal 016 |
| FR-012 | The timeout cascade MUST include at least `deadlines/work-by`, `deadlines/accept-by`, `deadlines/dispute-by`, and `deadlines/auto-release`. | Fact | Proposal 016 |
| FR-013 | When the responder delivers work, the system MUST open an acceptance window before final release unless the contract was canceled or expired earlier. | Inference | Proposal 016 |
| FR-014 | During the acceptance window, the payer MUST be able to confirm, reject within policy, or open a dispute. | Fact | Proposal 016 |
| FR-015 | If a valid dispute is opened before `deadlines/dispute-by`, the escrow supervisor MUST move the hold into `disputed` state and block auto-release until resolution. | Fact | Proposal 016 |
| FR-016 | If no dispute is open and acceptance conditions are satisfied until `deadlines/auto-release`, the escrow supervisor MUST release funds automatically. | Fact | Proposal 016 |
| FR-017 | The ledger MUST support explicit release, refund, and partial-release transfer kinds. | Fact | Proposal 016 |
| FR-018 | Partial release MAY be hidden from the first user-facing UI, but the artifact family MUST reserve a machine-readable representation for it. | Fact | Proposal 016 |
| FR-019 | Every internal movement of funds MUST be recorded as a `ledger-transfer` artifact. | Fact | Proposal 016 |
| FR-020 | Fiat-to-credit ingress and credit-to-fiat egress MUST each emit a `gateway-receipt` artifact. | Fact | Proposal 016 |
| FR-021 | `gateway-receipt` MUST identify the gateway node, direction, external amount/currency, internal amount/currency, the credited or debited account, and an external payment reference. | Fact | Proposal 016 |
| FR-022 | `procurement-receipt.v1` MUST continue to represent the contract-terminal outcome and MUST reference final settlement through `settlement/ref` rather than absorb all ledger detail. | Fact | Proposal 016 |
| FR-023 | A successful settlement MAY trigger a separate `reputation-signal.v1`, but the settlement path MUST NOT require such a signal to complete. | Fact | Proposal 016 |
| FR-024 | `UBC` allocations and `ubc_settlement` records MUST remain non-spendable for ordinary market procurement. | Fact | UBC policy |
| FR-025 | The system MUST reject paid procurement if the payer attempts to fund it from a protected floor or another non-spendable economic class. | Inference | UBC + separation rule |
| FR-026 | For `pod-client` flows, the serving node MAY act as gateway or settlement delegate, but the artifacts MUST preserve the split between host infrastructure actor and hosted economic owner. | Fact | Story 004 + Proposal 016 |

## Non-Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| NFR-001 | The supervised ledger MUST use atomic write semantics strong enough to prevent double-spend inside one federation MVP deployment. | Fact | Proposal 016 |
| NFR-002 | Economic contracts and receipts MUST stay auditable even when the external payment rail is implemented outside the protocol core. | Fact | Requirements 001 NFR-004 + Proposal 016 |
| NFR-003 | Gateway conversion policy MAY vary by federation or operator, but the protocol-visible procurement path MUST remain agnostic to fiat exchange logic. | Fact | Proposal 016 |
| NFR-004 | Every hold-, transfer-, and gateway-affecting artifact MUST be versioned and edge-validatable. | Inference | Contract-first architecture |
| NFR-005 | The MVP ledger model SHOULD remain append-only at the fact layer; balances are derived views, not the sole source of truth. | Inference | Proposal 016 + project values |
| NFR-006 | Timeout handling MUST eliminate indefinite fund blocking caused by silence of the payer, responder, or arbiter. | Fact | Proposal 016 |
| NFR-007 | Reputation and economic accounting MUST be auditable as separate accrual paths. | Fact | Sufficiency policy |
| NFR-008 | The settlement design MUST not require smart contracts, public-chain finality, or crypto-native custody in order to ship the first useful procurement MVP. | Fact | Proposal 016 |

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| Payer opens two contracts against the same balance | Double-spend and broken escrow | Enforce one authoritative ledger with atomic hold creation and available-balance checks. |
| Gateway credits balance without auditable fiat reference | Unreconcilable money boundary | Require `gateway-receipt` with external payment reference for every ingress or egress. |
| Responder delivers work but payer remains silent | Funds stay blocked forever | Enforce `accept-by`, `dispute-by`, and `auto-release` deadlines. |
| Payer confirms too quickly then finds a defect | Unfair release and weak recourse | Require a dispute-aware acceptance window and policy-defined cutoff semantics. |
| Partial work is delivered but only binary release exists | Manual ad hoc bookkeeping | Reserve `partial-release` in the transfer family from day one. |
| Economic balance becomes a hidden shortcut to influence | Constitutional drift | Enforce explicit conversion barriers and separate artifact families. |
| Protected compute floor is spent on market work | Exclusion of weaker participants | Treat protected floors such as `UBC` as non-spendable for procurement. |
| Split-brain supervisors appear in one federation MVP | Conflicting holds and balances | Make single authoritative ledger an explicit MVP deployment assumption. |

## Open Questions

1. Should `ledger-account` expose a spend-class or funds-class field in MVP, or is it enough to express spendability through account policy and gateway policy references?
2. Should the first MVP support outbound payout immediately, or only inbound top-up with manual off-ramp later?
3. What is the minimum arbiter policy when `confirmation/mode = arbiter-confirmed` and a dispute remains unresolved near `auto-release`?
4. Should `owner/kind = org` be reserved now in schema text, or deferred until the organization-identity proposal lands?

## Next Actions

1. Add the new settlement schema quartet:
   - `ledger-account.v1`
   - `ledger-hold.v1`
   - `ledger-transfer.v1`
   - `gateway-receipt.v1`
2. Extend `procurement-contract.v1` with escrow bindings and timeout cascade fields.
3. Extend `procurement-receipt.v1` with clearer settlement-reference guidance.
4. Add schema examples for:
   - funded account,
   - active hold,
   - settled release,
   - disputed hold,
   - refunded hold,
   - gateway top-up receipt.
5. Update solution-layer documents after the schemas land, especially the settlement-capable counterpart of `node.md`.
