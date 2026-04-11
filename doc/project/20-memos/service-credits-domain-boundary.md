# Service Credits Domain Boundary

Based on:
- `doc/normative/20-vision/en/VISION.en.md`
- `doc/normative/20-vision/pl/VISION.pl.md`
- `doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`
- `doc/project/50-requirements/requirements-007.md`

Date: `2026-04-10`
Status: Draft memo

## Purpose

This memo records that `service credits` are a domain-level economic concept and
should not be collapsed into the MVP settlement symbol `ORC`.

`ORC` is the current reference unit for the first supervised host-ledger MVP. It may
implement service-credit settlement in one federation, but it is not the whole
semantic contract of service credits.

## Working Definition

`Service credits` are an internal medium of exchange for voluntary service work in
the Orbiplex swarm.

They are used to:

- reserve value before paid service execution,
- settle accepted service delivery,
- refund or partially release value when the service path fails or is disputed,
- keep paid exchange auditable without turning balance into reputation or governance
  power.

Service credits belong to the service-exchange domain. They are separate from:

- reputation,
- `UBC` / protective compute floors,
- creator credits,
- emergency or rescue credits,
- external fiat money,
- public crypto assets or smart-contract-native tokens.

## Escrow Semantics

Escrow for service credits means a bounded hold over service-credit value for a
specific service contract.

The domain contract should describe:

- who funds the hold,
- who may receive release,
- which service contract the hold anchors,
- which policy controls dispute, timeout, partial release, release, refund, expiry,
  or freeze,
- which organization or node is accountable for supervision,
- which trace explains every transition.

The existing `ledger-hold.v1` artifact is the MVP host-ledger implementation shape
for this idea. A future `service-credit-hold` contract may either wrap it or make the
domain-level vocabulary explicit while keeping `ledger-hold.v1` as one concrete rail.

## Boundary With `ORC`

`ORC` should be treated as:

- the MVP reference symbol for one internal settlement unit,
- fixed-scale implementation detail of the first host-ledger rail,
- a concrete unit that can carry service-credit balances in MVP.

`ORC` should not be treated as:

- the generic name for all service credits,
- the only possible service-credit unit,
- a public monetary brand,
- a governance or reputation instrument.

The documentation should preserve this stratification:

- `service credits` = domain concept,
- `escrow hold` = domain mechanism,
- `ledger-hold.v1` = current concrete data contract,
- `ORC` = current MVP unit carried by that contract.

## Open Questions

1. Should service credits get a first-class schema, e.g. `service-credit-account.v1`
   or `service-credit-hold.v1`, or should the domain be documented through
   `ledger-account.v1`, `ledger-hold.v1`, and policy naming?
2. Should `ORC` be described as one federation-local service-credit unit, or as the
   hard-MVP reference unit only?
3. Should service-credit balances be visible in user-facing UI as "service credits"
   while protocol-visible artifacts keep `unit = ORC`?
4. Should escrow policies expose a domain field such as `credit/kind = service` to
   avoid confusing service exchange with UBC, creator credits, or rescue credits?

## Promote To

Promote this memo into a proposal or requirements update when the service-credit
vocabulary becomes implementation-facing, especially before changing settlement
schemas, UI terminology, or gateway/escrow policy fields.
