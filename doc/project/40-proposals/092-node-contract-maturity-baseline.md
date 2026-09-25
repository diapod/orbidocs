# Proposal 092: Node Contract Maturity Baseline

Based on:

- [Ontological Basis](../../normative/90-supplementary/en/ONTOLOGICAL-BASIS.en.md)
- [Core Values](../../normative/30-core-values/en/CORE-VALUES.en.md)
- [Vision](../../normative/20-vision/en/VISION.en.md)
- [Constitution](../../normative/40-constitution/en/CONSTITUTION.en.md)
- [Node](../60-solutions/000-node/000-node.md)
- `node:docs/implementation-ledger.toml`
- `node:docs/audits/CONTRACT-MATURITY-AUDIT-2026-09-20.md`

## Status

`accepted`

The operator requested the contract audit and accepted every bounded contract in
the audit manifest on 2026-09-20. This decision does not promote a referenced
draft proposal in its entirety and does not assert implementation completion or
release qualification.

## Date

`2026-09-20`

## Executive Summary

Accept the sixty previously unassessed Node ledger contracts as a repository
baseline. The accepted unit is the bounded contract expressed by one ledger row:
its capability identity, ownership, service/interface boundary, referenced data
contracts, current notes, and explicit exclusions in `next_steps`.

The Node audit records the per-row inspection and is the closed manifest for this
decision. This proposal supplies the upstream acceptance decision required by the
Node maturity vocabulary; the ledger remains the machine-readable source of
implementation status.

## Context and Problem Statement

The Node ledger acquired an independent `contract_maturity` axis after most of its
capability rows had already accumulated design, code, fixtures, tests, and runtime
evidence. Migration correctly initialized those rows as `unassessed`: working code
cannot silently accept its own contract.

Leaving the rows unassessed indefinitely would, however, conflate absent review
with rejected or unstable semantics. The requested audit therefore evaluates the
contract boundary of every such row against its upstream project artifacts and its
Node-side ownership and residual-work declarations.

## Decision

### 1. Accepted unit

For every capability listed in the dated Node audit, the following tuple is
accepted as the current contract:

`capability id + kind + owning crates/services + attached roles + based_on + schemas`

The row's `notes` explain the presently realized boundary. Its `next_steps` are
excluded work, not hidden acceptance criteria. A later semantic expansion requires
its own review even when it reuses the same capability id.

### 2. Evidence and authority remain stratified

Acceptance means that the contract is suitable to govern current Node work. It
does not mean that:

- the capability's `status` is `done`;
- its hard-MVP subset is complete;
- every referenced proposal is accepted as a whole;
- every optional or post-MVP path exists;
- historical tests qualify a current release candidate.

Draft parent proposals may therefore support an accepted, narrower ledger slice.
The narrower acceptance is owned here and must not be read back as proposal-wide
promotion.

### 3. Closed manifest

The manifest contains the sixty ledger rows whose maturity was `unassessed` at the
start of the audit. The constitutional exception record contract is deliberately
absent: it was already `draft` and retains its own promotion condition.

The canonical per-row list, rationale, repaired references, and exclusions live in
`node:docs/audits/CONTRACT-MATURITY-AUDIT-2026-09-20.md`. Every accepted row links
back to P092 in `based_on`, making the acceptance decision machine-auditable without
copying its full history into this proposal.

### 4. Change control

Editorial clarification and evidence updates do not invalidate acceptance when
they preserve the tuple and boundary above. Changes to authority, wire semantics,
ownership, required schema families, or declared service responsibility require a
new dated review and an upstream accepted decision before retaining `accepted`.

## Trade-offs

One baseline decision avoids sixty nearly identical proposals and keeps acceptance
separate from implementation bookkeeping. The cost is that readers must consult
the dated audit for row-level reasoning. Direct P092 references in every accepted
row make that indirection explicit and mechanically checkable.

Accepting bounded slices of draft parents permits useful stable contracts without
misrepresenting broader unfinished designs. It also requires disciplined wording:
the acceptance scope ends at the ledger row and its stated exclusions.

## Failure Modes and Mitigations

- **Implementation implies acceptance.** Mitigated by the independent maturity
  field and this explicit operator decision.
- **Slice acceptance promotes a whole draft proposal.** Mitigated by the bounded
  unit and proposal-wide non-promotion rule.
- **Residual work is silently accepted.** Mitigated by treating every `next_steps`
  item as excluded until separately reviewed.
- **Broken genealogy survives the audit.** Mitigated by resolving every `based_on`
  path and correcting legacy short filenames before promotion.
- **Release readiness is inferred.** Mitigated by leaving candidate-bound
  qualification and the independent implementation/hard-MVP axes untouched.

## Open Questions

None for this baseline. New or materially expanded contracts return to
`unassessed` or `draft` until their owning decision is accepted.

## Next Actions

1. Keep the Node audit and generated ledger view synchronized with the authored
   TOML ledger.
2. Done on 2026-09-25: `node:tools/implementation_ledger.py` requires every
   accepted row to name an id from the closed `acceptance_decisions` table whose
   document is also in the row's `based_on`, refuses decisions on non-accepted
   rows and unused decisions, and with `--orbidocs PATH` resolves each decision
   document. The check immediately found the P091 foundation row accepted without
   a decision; the operator then accepted the bounded P091-002 freeze in P091.
3. Review future semantic expansions independently from implementation and release
   qualification.
