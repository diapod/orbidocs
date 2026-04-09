# Story 006 Settlement Rail Sprint 3

Based on:
- `doc/project/30-stories/story-006.md`
- `doc/project/30-stories/story-006-buyer-node-components.md`
- `doc/project/20-memos/service-order-to-procurement-bridge.md`
- `doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`
- `doc/project/50-requirements/requirements-007.md`
- `doc/project/50-requirements/requirements-008.md`
- `doc/project/60-solutions/node.md`

Date: `2026-03-30`
Status: Accepted hard-MVP planning note

## Purpose

This memo freezes the hard-MVP settlement rail needed by `story-006` after the
service-offer catalog and buyer-side service-order bridge.

The scope is deliberately narrow:

- one deployment-local supervised ORC ledger,
- one operator-driven top-up path,
- one hold state machine owned by the buyer-side Node host,
- and one append-only fact model that avoids rollback folklore.

It does **not** yet freeze a final remote buyer-to-escrow wire protocol.

## Hard-MVP Decisions

### 1. Deployment-local settlement authority

For hard MVP:

- catalog and escrow ledger live inside the Node daemon,
- gateway may run as a separate local process on the same host when fiat ingress
  is needed,
- Node talks to gateway through an explicit local adapter,
- there is no requirement yet for a remote buyer-to-escrow protocol.

### 2. Lazy account creation

Ledger accounts are created lazily.

This means:

- reading a missing account returns zero balance,
- missing account during hold precheck is treated as insufficient funds,
- the buyer bridge maps that outcome to `settlement-blocked`,
- the ledger does **not** raise `AccountNotFound` for the hard-MVP buyer path.

Frozen local account namespace for hard MVP:

- `account:{identity_id}` for identity-backed settlement accounts
  (`participant:...`, `org:...`, and later other identity namespaces),
- `account:community-pool` for the shared system pool.

### 3. ORC arithmetic uses integer minor units only

`ORC` arithmetic MUST NOT use floating-point numbers.

Hard-MVP freeze:

- `ORC` uses fixed decimal scale `2`,
- ledger and bridge arithmetic use integer minor units only,
- display formatting into `major.minor` lives in read or presentation layers,
- no temporary conversion through `f64` is admissible.

### 4. Hold creation is append-only, not transactional rollback

Hold creation and execution opening are modeled as append-only facts rather than a
two-phase commit.

Bridge sequence:

1. read-side balance precheck,
2. append `HoldCreated`,
3. open execution carrying `hold_id`,
4. if execution opening fails, append `HoldVoided`.

The hard-MVP deployment-local ledger may use a mutex around ledger mutation to
reduce concurrent submission races, but the semantic model remains append-only.

### 5. Gateway receipt idempotency

The same `gateway-receipt/id` MUST NOT credit a local account more than once.

Hard-MVP write path:

- top-up ingestion deduplicates by `gateway-receipt/id`,
- the first application credits the account,
- later repeats return an idempotent already-applied outcome,
- no second credit transfer is recorded.

### 6. Hold state machine includes dispute freeze from the start

Hard-MVP hold states:

- `active`
- `frozen`
- `released`
- `refunded`
- `voided`

Required transitions:

- `active -> released`
- `active -> refunded`
- `active -> frozen`
- `active -> voided`
- `frozen -> released`
- `frozen -> refunded`

This keeps dispute handling explicit without refactoring the settlement rail later.

### 7. Settlement ledger is trait-owned

The daemon must depend on a thin behavior contract rather than a concrete inline
implementation.

Recommended shape:

```rust
pub trait SettlementLedger: Send + Sync {
    fn balance(&self, account: &AccountId) -> Result<OrcBalance, LedgerError>;
    fn apply_top_up(
        &self,
        receipt: &GatewayReceiptRecord,
    ) -> Result<TopUpApplyOutcome, LedgerError>;
    fn create_hold(&self, spec: HoldSpec) -> Result<HoldRecord, LedgerError>;
    fn void_hold(&self, id: &HoldId, reason: &str) -> Result<HoldRecord, LedgerError>;
    fn release_hold(&self, id: &HoldId) -> Result<HoldRecord, LedgerError>;
    fn refund_hold(&self, id: &HoldId) -> Result<HoldRecord, LedgerError>;
    fn freeze_hold(&self, id: &HoldId) -> Result<HoldRecord, LedgerError>;
    fn hold_status(&self, id: &HoldId) -> Result<Option<HoldRecord>, LedgerError>;
}
```

Hard-MVP implementation:

- `LocalOrcLedger`

Post-MVP freedom:

- remote escrow adapter,
- richer payout rail,
- alternative local storage implementation.

### 8. Top-up is operator-only in hard MVP

`POST /v1/ledger/top-up` is an operator surface guarded by the control-plane
auth token.

For hard MVP:

- `Arca` does not invoke top-up directly,
- top-up does not yet require a middleware-facing classified result,
- custodian-aware self-service top-up may be added later as a separate capability.

## Data and Fact Model

The settlement rail should own append-only facts such as:

- `ledger/top-up-applied.v1`
- `ledger/hold-created.v1`
- `ledger/hold-voided.v1`
- `ledger/hold-frozen.v1`
- `ledger/hold-released.v1`
- `ledger/hold-refunded.v1`

Read models are derived from those facts:

- account balance view,
- hold status view,
- top-up history,
- release or refund history.

## Integration With The Buyer Bridge

The buyer bridge already owns:

- active offer resolution,
- order-to-offer sequence check,
- price and units computation,
- organization custodian resolution,
- settlement preflight gating,
- execution opening,
- buyer-local marketplace lineage.

Sprint 3 adds the settlement rail beneath that bridge:

- price computation yields one ORC minor-unit amount,
- settlement preflight reads lazy account balance,
- hold creation reserves value before execution open,
- execution state keeps `hold_id`,
- later procurement closure transitions the hold into release, refund, or freeze.

The bridge remains host-owned. `Arca` still does not author settlement facts.

## Planned Implementation Order

### A. Domain types and trait

Add one workspace crate for:

- `AccountId`
- `HoldId`
- `OrcAmount` / `OrcBalance`
- `HoldSpec`
- `HoldRecord`
- `GatewayReceiptRecord`
- `LedgerFact`
- `LedgerError`
- `SettlementLedger`

### B. `LocalOrcLedger`

Implement:

- append-only facts,
- in-memory projector,
- restore-on-open semantics,
- lazy account balances.

### C. Top-up write path

Add operator-only top-up ingestion with idempotent deduplication by
`gateway-receipt/id`.

### D. Buyer-bridge hold integration

Add:

- balance precheck,
- `HoldCreated`,
- execution open carrying `hold_id`,
- `HoldVoided` on failed open.

### E. Release and refund path

Tie terminal procurement outcomes to:

- `HoldReleased`
- `HoldRefunded`

### F. Dispute freeze path

Tie dispute opening and dispute resolution to:

- `HoldFrozen`
- then `HoldReleased` or `HoldRefunded`

### G. Control surface

Read-side minimum:

- `GET /v1/ledger/account`
- `GET /v1/ledger/holds/{id}`

### H. Launcher wrapping

Thin launcher and CLI surfaces:

- top-up submit,
- account inspect,
- hold inspect.

## Done Criteria For Sprint 3

The settlement-rail slice should be considered closed for hard MVP when:

- ORC arithmetic stays integer-only,
- top-up is idempotent by `gateway-receipt/id`,
- lazy account semantics are live,
- buyer bridge can create a hold before execution open,
- failed execution open voids the hold,
- settled and refunded outcomes transition holds explicitly,
- dispute freezes the hold instead of silently leaving it active,
- operator read surfaces expose account and hold state without spelunking trace.
