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
- `Payee`: participant or organization receiving payment after successful delivery.
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
  - `hold/id`, `contract/id`, `payer/account-id`, `payee/account-id`,
    `escrow/node-id`, `amount`, `unit`, `status`, `created-at`, `work-by`,
    `accept-by`, `dispute-by`, `auto-release-after`.
- `LedgerTransfer`:
  - `transfer/id`, `kind`, `from/account-id`, `to/account-id`, `amount`, `unit`,
    `created-at`, optional `hold/id`, optional `contract/id`,
    optional `gateway-receipt/id`.
- `GatewayReceipt`:
  - `receipt/id`, `gateway/node-id`, `direction`, `external/amount`,
    `external/currency`, `internal/amount`, `internal/currency`, `account/id`, `ts`,
    `external/payment-ref`, `gateway-policy/ref`, optional `exchange-policy/ref`.
- `GatewayPolicy`:
  - `policy/id`, `federation/id`, `gateway/node-id`, `operator/org-ref`,
    `settlement/unit`, `supported/directions`, `status`, `created-at`.
- `EscrowPolicy`:
  - `policy/id`, `federation/id`, `escrow/node-id`, `operator/org-ref`,
    `settlement/unit`, `confirmation/modes`, `dispute/default-window-sec`,
    `auto-release/default-sec`, `partial-release/allowed`, `status`, `created-at`.
- `SettlementPolicyDisclosure`:
  - `disclosure/id`, `recorded-at`, `effective/from`, optional `effective/until`,
    `federation/id`, `policy/ref`, `operator/org-ref`, `serving/node-id`,
    `event/type`, `disclosure/scope`, `impact/mode`, `reason/summary`,
    optional `case/ref`, optional `exception/ref`, optional `basis/refs`.
- Extensions to `ProcurementContract`:
  - `payer/account-ref`, `payee/account-ref`, `escrow/node-id`,
    `escrow/hold-ref`, `escrow-policy/ref`, `deadlines/work-by`, `deadlines/accept-by`,
    `deadlines/dispute-by`, `deadlines/auto-release`.
  - `payer/account-ref` and `payee/account-ref` are canonical role-prefixed
    settlement subject references, so separate `payer/kind` and `payee/kind`
    fields are intentionally excluded.
- Extension to `ProcurementReceipt`:
  - explicit links from `settlement/ref`, `settlement/hold-ref`, and optional
    `settlement/transfer-refs` to final ledger outcome facts.

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
| FR-004 | The system MUST support a `ledger-account` artifact that binds an account to an accountable owner, settlement unit, and account purpose. | Fact | Proposal 016 |
| FR-005 | `ledger-account` ownership MUST support at least `participant`, `pod-user`, and `org` as owner kinds. | Fact | Story 004 + Proposal 016 + Proposal 017 |
| FR-005a | `ledger-account` MUST admit `account/purpose = community-pool` as a first-class host-ledger account owned by an accountable `org` subject and controlled for disbursement by a canonical `council:did:key:...` in MVP. | Fact | Proposal 016 + nym/council baseline |
| FR-006 | The system MUST perform an available-balance precheck before creating a paid procurement contract. | Fact | Requirements 001 FR-015 + Proposal 016 |
| FR-007 | When balance is sufficient, the escrow supervisor MUST create a `ledger-hold` before remote paid execution begins. | Fact | Proposal 016 |
| FR-008 | `ledger-hold` MUST include explicit status and timeout fields for work, acceptance, dispute, and auto-release. | Fact | Proposal 016 |
| FR-009 | `ledger-hold.status` MUST support at least `active`, `disputed`, `released`, `partially-released`, `refunded`, and `expired`. | Fact | Proposal 016 |
| FR-010 | `procurement-contract.v1` MUST gain explicit settlement bindings: `payer/account-ref`, `payee/account-ref`, `escrow/node-id`, and `escrow/hold-ref`. | Fact | Proposal 016 |
| FR-010a | `payer/account-ref` and `payee/account-ref` MUST be canonical role-prefixed settlement subject references, and `procurement-contract.v1` MUST NOT duplicate that role through separate `payer/kind` or `payee/kind` fields. | Fact | Proposal 016 + Proposal 017 |
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
| FR-020a | Inbound `gateway-receipt` artifacts MUST disclose gross external amount, explicit external fee amount, fee rate, fee destination account, net external amount, applied conversion rate, net internal credited amount, and internal fee amount rather than hiding the community contribution inside the rate. | Fact | Proposal 016 |
| FR-020b | Inbound top-up settlement MUST atomically record both the net credit to the payer account and the fee credit to the `community-pool` account from one gateway event. | Fact | Proposal 016 |
| FR-020c | `gateway-receipt.v1` MUST be signed by the serving gateway node over a stable deterministic payload excluding only the `signature` field itself. | Fact | Proposal 016 |
| FR-021 | `gateway-receipt` MUST identify the gateway node, direction, external amount/currency, internal amount/currency, the credited or debited account, an external payment reference, and the governing `gateway-policy/ref`. | Fact | Proposal 016 |
| FR-021a | The system MUST support a `gateway-policy` artifact that binds a serving gateway node to an accountable `operator/org-ref` and the admitted settlement directions. | Fact | Proposal 016 + Proposal 017 |
| FR-021b | The system MUST support an `escrow-policy` artifact that binds a serving escrow node to an accountable `operator/org-ref` and the default dispute and release semantics. | Fact | Proposal 016 + Proposal 017 |
| FR-021ba | `gateway-policy.v1` MUST publish a fixed MVP ingress fee rate, an ingress fee destination account id, and a minimum internal amount below which ingress fee is not applied. | Fact | Proposal 016 |
| FR-021bb | `gateway-policy.v1` MAY expose `fee/egress-rate`, but the first MVP SHOULD keep it `null` until the outbound payout path stabilizes. | Fact | Proposal 016 |
| FR-021c | The system MUST support a `settlement-policy-disclosure` artifact for auditable policy-facing events such as suspension, reinstatement, limit changes, manual-review enforcement, or settlement incidents affecting a `gateway-policy` or `escrow-policy`. | Fact | Proposal 016 + ABUSE-DISCLOSURE-PROTOCOL |
| FR-021d | `settlement-policy-disclosure` MUST snapshot the affected `policy/ref`, the accountable `operator/org-ref`, the observed `serving/node-id`, the disclosure scope, and the practical impact mode at event time. | Fact | Proposal 016 + Proposal 017 |
| FR-021e | `incident/*` settlement-policy disclosures MUST carry at least one formal audit anchor through `case/ref`, `exception/ref`, or non-empty `basis/refs`. | Fact | Proposal 016 + ABUSE-DISCLOSURE-PROTOCOL |
| FR-021f | Gateway or escrow policy MAY refuse a paid path, restrict regions, restrict account classes, or disable one rail, but any policy-facing `manual-review-only` or `blocked` path MUST disclose whether it is bounded by policy, case, or exception rather than leaving the gate as implicit operator grace. | Fact | Proposal 016 + Constitution Art. II |
| FR-021g | Settlement policy artifacts and disclosures MUST NOT model humiliation, self-abasement, emotional dependency, or other non-policy personal submission as an admissible access condition. Such behavior MUST be represented as a settlement incident rather than as a valid review mode. | Fact | Constitution Art. II + UBC policy + EXCEPTION-POLICY |
| FR-022 | `procurement-receipt.v1` MUST continue to represent the contract-terminal outcome and MUST reference final settlement through `settlement/ref` rather than absorb all ledger detail. | Fact | Proposal 016 |
| FR-023 | A successful settlement MAY trigger a separate `reputation-signal.v1`, but the settlement path MUST NOT require such a signal to complete. | Fact | Proposal 016 |
| FR-024 | `UBC` allocations and `ubc_settlement` records MUST remain non-spendable for ordinary market procurement. | Fact | UBC policy |
| FR-025 | The system MUST reject paid procurement if the payer attempts to fund it from a protected floor or another non-spendable economic class. | Inference | UBC + separation rule |
| FR-026 | For `pod-client` flows, the serving node MAY act as gateway or settlement delegate, but the artifacts MUST preserve the split between host infrastructure actor and hosted economic owner. | Fact | Story 004 + Proposal 016 |
| FR-027 | `ledger-hold` and `procurement-contract.v1` on the `host-ledger` rail MUST reference the governing `escrow-policy/ref`. | Fact | Proposal 016 + Proposal 017 |
| FR-028 | Community-pool disbursements in MVP MUST remain basis-anchored ledger facts and MUST NOT target governance rewards, creator credits, or reputation accrual. | Fact | Constitution Art. XII + Proposal 016 |
| FR-028a | The system MUST support a `community-pool-disbursement.v1` artifact that binds one `community-pool` outflow to a destination account, one admitted purpose, non-empty `basis/refs`, a resulting `ledger-transfer/id`, and a canonical `council:did:key:...` approver. | Fact | Proposal 016 |
| FR-028b | `community-pool-disbursement.v1` MUST support only `ubc-subsidy`, `infrastructure-support`, and `emergency-relief` as first MVP purposes. | Fact | Proposal 016 |

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
| NFR-009 | Settlement-policy disclosures MUST remain append-only audit facts and MUST NOT replace the underlying gateway or escrow policy artifact. | Fact | Proposal 016 + project values |
| NFR-010 | Public or federation-scoped settlement disclosures MUST stay bounded by minimal necessary disclosure and SHOULD prefer redacted scopes unless stronger exposure is operationally required. | Fact | ABUSE-DISCLOSURE-PROTOCOL |
| NFR-011 | Settlement review paths MUST stay auditable enough to distinguish bounded refusal from arbitrary discretionary gatekeeping. | Inference | Constitution Art. II + Proposal 016 |
| NFR-012 | Gateway fee collection and community-pool disbursement MUST remain auditable as separate signed or basis-anchored fact paths rather than as implicit balance mutations. | Inference | Proposal 016 + project values |

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| Payer opens two contracts against the same balance | Double-spend and broken escrow | Enforce one authoritative ledger with atomic hold creation and available-balance checks. |
| Gateway credits balance without auditable fiat reference | Unreconcilable money boundary | Require `gateway-receipt` with external payment reference for every ingress or egress. |
| Community fee is hidden inside spread or disappears into operator revenue | Extraction becomes opaque and unauditable | Require explicit fee fields, applied rate, and atomic split to the `community-pool` account. |
| Responder delivers work but payer remains silent | Funds stay blocked forever | Enforce `accept-by`, `dispute-by`, and `auto-release` deadlines. |
| Payer confirms too quickly then finds a defect | Unfair release and weak recourse | Require a dispute-aware acceptance window and policy-defined cutoff semantics. |
| Partial work is delivered but only binary release exists | Manual ad hoc bookkeeping | Reserve `partial-release` in the transfer family from day one. |
| Economic balance becomes a hidden shortcut to influence | Constitutional drift | Enforce explicit conversion barriers and separate artifact families. |
| Protected compute floor is spent on market work | Exclusion of weaker participants | Treat protected floors such as `UBC` as non-spendable for procurement. |
| Split-brain supervisors appear in one federation MVP | Conflicting holds and balances | Make single authoritative ledger an explicit MVP deployment assumption. |
| Gateway or escrow policy is suspended without a durable disclosure trail | Operators and counterparties cannot reconstruct why settlement degraded or stopped | Require append-only `settlement-policy-disclosure` events with scope, impact, and audit anchors. |
| Manual review degrades into opaque operator favor or abusive access conditions | Voluntary exchange mutates into dignity-unsafe gatekeeping | Require bounded review basis in disclosure artifacts and classify abusive access conditions as settlement incidents. |

## Open Questions

1. Should `ledger-account` expose a spend-class or funds-class field in MVP, or is it enough to express spendability through account policy and gateway policy references?
2. Should the first MVP support outbound payout immediately, or only inbound top-up with manual off-ramp later?
3. What is the minimum arbiter policy when `confirmation/mode = arbiter-confirmed` and a dispute remains unresolved near `auto-release`?
4. When `pod-user:did:key:...` is enabled for direct paid procurement, should policy admit it immediately as a first-class `account-ref`, or only through a hosting participant or organization?

## Next Actions

1. Roll `org` into the highest-value accountability schemas beyond settlement, starting with `reputation-signal.v1`.
2. Add a dedicated organization subject artifact or schema fragment that carries `org/custodian-ref`.
3. Decide when `pod-user:did:key:...` becomes an operationally supported `account-ref` in paid procurement rather than only a forward-compatible identifier family.
4. Update solution-layer documents after the schemas land, especially the settlement-capable counterpart of `node.md`.
