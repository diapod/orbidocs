# Story 007: Settlement-Capable Node as the Authoritative ORC Ledger

## Current Baseline Used by This Story

This story is the operator-facing settlement counterpart of `story-001.md`. It is
based on the current supervised-ledger corpus rather than on an imagined later
payment system.

In particular, it assumes:

- one federation-local authoritative host-ledger instance for MVP, understood
  as one logical settlement authority rather than necessarily one physical host,
- explicit separation between:
  - routing identities (`node-id`),
  - participation subjects (`participant:did:key:...`),
  - organization subjects (`org:did:key:...`),
  - and settlement accounts (`ledger-account.v1`),
- `ORC` as the internal settlement unit visible to procurement artifacts, with
  fixed decimal scale `2` and protocol-visible integer amount fields expressed in
  ORC minor units,
- trusted gateway and escrow roles attached to a settlement-capable Node,
- append-only settlement facts instead of hidden mutable balance state,
- explicit `gateway-policy.v1`, `escrow-policy.v1`, and
  `settlement-policy-disclosure.v1` artifacts,
- procurement contracts that bind the business agreement to explicit settlement
  anchors such as `payer/account-ref`, `payee/account-ref`, `escrow/node-id`, and
  `escrow/hold-ref`.

This story does not assume a public-chain rail, decentralized smart contracts, or
cross-federation settlement portability.

## Sequence of Steps

1. An umbrella organization decides to run one Node in the
   `settlement-capable` deployment profile for one federation.
2. The operator starts the Node with settlement services enabled and binds it to a
   stable local `node-id` plus a stable accountable organization subject
   `org:did:key:...`.
3. The operator publishes or loads the current `gateway-policy.v1` and
   `escrow-policy.v1` artifacts, each naming:
   - the serving node,
   - the accountable `operator/org-ref`,
   - the admitted settlement unit `ORC`,
   - and the active status and timing semantics.
4. The settlement-capable Node creates or restores the authoritative ledger scope
   for that federation. This scope may later be implemented with failover or HA,
   but in MVP the only frozen constraint is that it behaves as one logical
   authority and single-writer ledger. Within this scope it treats
   `ledger-account.v1` as the canonical binding between an accountable subject and
   one ORC account.
5. The operator provisions the first accounts:
   - a `community-pool` account owned by the accountable organization,
   - one or more `participant-settlement` accounts for participants,
   - and, where needed later, `org-settlement` accounts for organizations serving
     as payees.
6. When a new participant is admitted to paid procurement, the Node creates a
   `ledger-account.v1` whose `owner/id` is the canonical accountable subject such as
   `participant:did:key:...` rather than the raw `node-id`.
7. The operator or a connected payer performs a prepaid top-up through the gateway
   path. The gateway side receives external money and emits one signed
   `gateway-receipt.v1`.
8. From that gateway event, the authoritative ledger records the corresponding
   append-only internal facts:
   - one net credit to the payer's settlement account,
   - and, when policy requires it, one fee credit to the `community-pool` account.
9. The payer opens a priced procurement flow elsewhere in the swarm. The resulting
   `procurement-contract.v1` names:
   - `payer/account-ref` as the accountable economic owner,
   - `payee/account-ref` as the accountable receiving owner,
   - `settlement/rail = host-ledger`,
   - and the escrow anchors for this contract.
10. Before remote execution begins, the settlement-capable Node checks available
    balance for the payer's account. This check is against the authoritative ledger
    view, not against chat-local state or offer-local assumptions.
11. If balance is sufficient, the Node creates one `ledger-hold.v1` that reserves
    the ORC amount on the payer account for that exact contract.
12. The contract and the hold are now joined in both directions:
    - the hold names `contract/id`,
    - the contract names `escrow/hold-ref`.
13. While the responder works, the ledger remains the source of truth for the
    reserved amount, dispute window, and timeout cascade:
    - `work-by`,
    - `accept-by`,
    - `dispute-by`,
    - `auto-release-after`.
14. When the responder delivers, the payer confirms, rejects within policy, or
    opens a dispute. If silence persists until the contract policy allows it,
    auto-release may occur.
15. The settlement-capable Node then records one or more `ledger-transfer.v1`
    facts, for example:
    - `release` to the payee account,
    - `partial-release` plus `refund`,
    - or full `refund` to the payer account.
16. A `procurement-receipt.v1` records the terminal business outcome and points back
    to the settlement path through `settlement/ref`, `settlement/hold-ref`, and
    optional `settlement/transfer-refs`.
17. At any moment, the Node can export an operator-visible read model for each
    account, such as current `available/balance` and `held/balance`, but those
    remain derived views rather than the only source of truth.
18. If the organization suspends payouts, imposes manual review, or blocks a
    settlement path, the Node emits `settlement-policy-disclosure.v1` rather than
    silently mutating behavior. Paid procurement then becomes:
    - `blocked`,
    - `manual-review-only`,
    - or otherwise degraded,
    while preserving audit joins to the governing policy.
19. If the organization later needs to support an accountable service provider or
    collective payee, it provisions an `org-settlement` account whose `owner/id` is
    `org:did:key:...`. ORC therefore remains attached to the organization's ledger
    account, not to an informal label or to the serving infrastructure node.
20. If the federation operator needs to inspect a balance anomaly, dispute, or
    complaint, the Node can reconstruct it from append-only artifacts:
    - `gateway-receipt.v1`,
    - `ledger-hold.v1`,
    - `ledger-transfer.v1`,
    - `procurement-contract.v1`,
    - `procurement-receipt.v1`,
    - and any `settlement-policy-disclosure.v1` events.

## Implementation Guidance Carried by This Story

- ORC ownership belongs to `ledger-account.v1`, not directly to `participant` or
  `org` records.
- ORC uses fixed scale `2`: protocol-visible integers carry minor units, while
  human-facing rendering uses `major.minor ORC`.
- `participant:did:key:...` and `org:did:key:...` are accountable owners; the
  ledger account is the settlement container.
- `available/balance` and `held/balance` are exported read models, not the only
  source of truth.
- The first settlement-capable runtime should prefer one authoritative ledger per
  federation over multi-supervisor split-brain complexity.
- MVP does not yet freeze a concrete HA profile beyond one logical authority and no
  split-brain behavior.
- The storage backend may later be swapped for MariaDB or a similar replicated
  engine if the ledger still preserves append-only facts, one logical authority, and
  protocol-visible compatibility.
- Gateway and escrow behavior should remain policy-bound and disclosure-friendly,
  not hidden inside ad hoc operator grace.

## Open Continuation

- Multi-supervisor federation once one-ledger MVP is stable.
- Cross-federation settlement portability.
- Operational support for direct `pod-user:did:key:...` ownership in paid paths.
- First user-facing operator UI for inspecting ledger accounts, holds, transfers,
  and policy disclosures together.
