# Whisper Contract Review — 2026-10-28

Status: design corrections; runtime gates remain open.

Based on:
- [P013](../013-whisper-social-signal-exchange.md)
- [P015](../015-nym-certificates-and-renewal-baseline.md)
- [Story 014](../../30-stories/story-014-dormant-contest-entry.md)

## Executive Summary

The review covers the documentation introduced from Orbidocs
`9946ba306132cce7c78877ab0363c76dd10d675b` through
`8f572e5e` (the input revision). Participant agency and bounded disclosure become
an independently signed author manifest, a single case-ordering authority and
recipient-bound AD delivery. Consent, cryptographic authenticity and delivery
remain separate claims. No schemas, runtime code or historical evidence are
changed by this review; prospective contract names below are not deployed types.

## Context and Decisions

All F-01–F-24 findings were confirmed against that input, with these qualifications:
F-04 was an underspecified product choice; the chosen rule is per concrete audience
**descriptor**, not class. F-11 is an explicit Phase 1 suite, not instant algorithm
agility. F-15 is propagation of an already proposed narrow MVP requirement, not a
runtime completion claim. F-19 renames only prospective embargo artifacts; existing
holder-assisted `whisper-disclosure-request/decision.v1` names remain unchanged.

| Finding | Decision and owner | Qualifying task / check |
|---|---|---|
| F-01 | ADC owns detached nym-signed manifest; P015 owns signing scope; P035 receipt binds full private admission to manifest | ADC-001/005, P015-005, P035-019; S014-A17 verifies offline with private retrieval denied |
| F-02 | LLR now states invariants, trade-offs, failures and open questions | LLR-002/003/006/008 refusal/recovery gates |
| F-03 | ADC protected holders = named correlators union counting authority; AD checks role-bound recipients | ADC-003, PEX-001; S014-A18 separates nodes C and D |
| F-04 | ADC slot = original condition digest + canonical audience descriptor digest; route is separate | ADC-005; S014-A16 tests two rooms and two routes |
| F-05 | ADC invariant permits only approved payload, criterion/count metadata and minimal proof; private proof fields excluded | ADC-001/005; S014-A15 canary/proof-field scan |
| F-06 | ADC separates active condition, declined proposal and committed execution; all pre-commit waits allow withdrawal/expiry | ADC-005/008; S014-A19 plus both race orders in A13 |
| F-07 | LLR anchor has zero/one original condition; narrower keeps slots, wider creates new case without inherited consent or silent withdrawal | ADC-001, LLR-006; S014-A20 |
| F-08 | DFR relation targets public notice id with explicit kind; Harvester does not expose private anchor | DFR-004, ADC-007, P078-012; S014-A21 |
| F-09 | P013-PEX-001 owns private exchange over existing AD/INAC | Two-node recipient/refusal/replay/restart/expiry gate; no new transport |
| F-10 | LLR-006 owns key commitment, ADC-001 consumes it; no reverse task dependency | Tracker dependency audit; key mismatch/loss fixtures in LLR-006 |
| F-11 | P015/LLR name Ed25519 as closed Phase 1 suite; two authorization roles stay semantic | P015-004 vectors; P081 adapter re-use, no arbitrary alg |
| F-12 | P015-005 owns issuance and verification of bound publication tuples and explicit manifest signing use | Wrong-kind/schema/topic/scope and signature-use confusion fixtures |
| F-13 | ADC later epochs require N + 1 even if author absent; succession does not identify sources | ADC-004; S014-A14, UI threshold explanation |
| F-14 | P036 co-retains proof and bytes, S026 owns key custody/recovery opt-in, P070 binds concrete room/history consent | LLR-003/006 and ADC-005 integration gates linked from consumers |
| F-15 | P015-004 remains todo MVP schema/pure verifier only; snapshot, Node MVP, ledger and executable alpha membership agree | Node ledger/profile validation; generated ledger; no full LLR MVP claim |
| F-16 | P015 v1 stays current until the coordinated P015-004 migration closes | Gate includes schema/example/references/generated coverage/Node acceptance migration |
| F-17 | S020 opens epoch window; Whisper owns persisted entry offsets; AD purge is separate maintenance | DFR-002/CIM-003 timing replay and S023-002 retention gates |
| F-18 | Link directly to S011 implementation Layer 7's aggregate-only promotion rule | Document link validation |
| F-19 | New candidate family is whisper-embargo-*; holder redistribution keeps whisper-disclosure-request/decision | Search for stale candidate names; no schema/evidence rewrite |
| F-20 | ADC-000 names DFR-002/003/006, PEX-001 and P015-005; Story owns assertion/task/evidence matrix | Dependency and matrix checks; composed report still pending |
| F-21 | Story lists cross-epoch counting, author reachability and hidden-count trust limits | Story open continuation; no qualification beyond current variant |
| F-22 | P013 keeps domain map and compatibility anchors; ADC/CIM/LLR move to sidecars in a separate structural commit | Normalized content comparison and inbound link/anchor checks |
| F-23 | S011 fixes punctuation, names P035 receipt owner and points to commit-based release | S011 link and terminology review |
| F-24 | satisfied is derived proposal evidence, never durable case status | ADC-008; S014-A19 |

Task shorthand in this table expands to `P013-<prefix>-<number>`; other P/S
identifiers retain their repository meaning. Full gates live with their owner,
not in this review.

Two additional corrections follow from the same audit: a commit receipt must
bind a pre-commit **intent**, not a final envelope containing that receipt (hash
cycle); and source-owned P036-006/008 contracts must precede P078-013/DFR-003
consumers rather than depend on them in return. P035-019 similarly consumes the
P015 publication-time **contract**, not completed P041/Whisper runtime consumers.

## Trade-offs

A detached manifest permits offline verification with less disclosure, but the
receiver still trusts the admitted authority for the hidden signal/count. A case
key extends control beyond nym expiry and extends its compromise window. A slot
per descriptor is more precise than a class-wide slot and requires canonical,
explicit audience consent. None of these decisions establishes psychological
independence, truth or global knowledge of revocation.

## Failure Modes and Mitigations

The blocking future proofs are S014-A13 and A15–A21: missing private-body access,
wrong manifest, distinct holder roles, audience aliasing, expiry, both race orders,
lost reply and crash before AD. Missing evidence leaves the corresponding tracker
open. The authority orders consent once; AD recovery never re-decides it.

## Open Questions

ADC retains cross-epoch distinctness, count proofs independent of the authority,
reachability and capacity/profile bounds. LLR retains authority replacement and
independent compromise recovery as separate future designs. These are not patched
with optimistic fallbacks or hidden participant mappings.

## Next Actions

Freeze LLR-006 and P015-005/P035-019 contracts before ADC-001; qualify the shared
PEX-001 carrier independently of its consumers. Implement and retain the named
negative proofs before closing the Story variant. P015-004's pure verifier is a
separate narrow MVP obligation. Keep the structural extraction in a separate
commit so this semantic change remains reviewable.
