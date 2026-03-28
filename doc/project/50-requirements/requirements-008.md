# Requirements 008: Organization Subject Rollout and Custody Baseline

Based on:
- `doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`
- `doc/project/20-memos/reputation-signal-v1-invariants.md`
- `doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`
- `doc/normative/50-constitutional-ops/pl/ROOT-IDENTITY-AND-NYMS.pl.md`
- `doc/normative/50-constitutional-ops/pl/PROCEDURAL-REPUTATION-SPEC.pl.md`

Date: `2026-03-28`
Status: Draft (rollout baseline)

## Executive Summary

This document defines the first implementation-facing requirements for
organization-scoped subjects in Orbiplex.

The rollout goal is narrow and deliberate:

- freeze the canonical organization identifier family,
- admit `org` into accountable procedural and contract paths,
- preserve the distinction between organizational accountability and pseudonymous
  social-layer participation,
- and define the minimal MVP custody model for organization subjects.

## Context and Problem Statement

Orbiplex already uses stable role-prefixed identity families:

- `node:did:key:...`
- `participant:did:key:...`
- `nym:did:key:...`
- `council:did:key:...`

The new settlement and procurement layer exposes a missing institutional actor:

- some paid counterparts may be organizations rather than individuals,
- some gateways or escrow providers may be run under organizational
  responsibility,
- some procedural or contract-domain signals should land on an organization
  rather than be forced onto one employee's `participant:did:key`.

Without a distinct organization subject family, the system would either:

- overload `participant` with institutional semantics,
- or misuse `nym` as an accountability vehicle.

Both outcomes are architecturally wrong.

## Proposed Model / Decision

### Canonical Identifier Family

The canonical organization identifier format is:

`org:did:key:z<base58btc(0xed01 || raw_ed25519_public_key)>`

This continues the existing role-prefixed DID convention. Therefore:

- `org:did:key:...` is canonical,
- `org-id:did:key:...` is non-canonical for v1.

### MVP Custody Baseline

An organization subject may be administered by one designated human-side
custodian in MVP:

- `subject/kind = org`
- `subject/id = org:did:key:...`
- `org/custodian-ref = participant:did:key:...`

Threshold or multisig custody is deferred.

### Rollout Boundary

In MVP, `org` is an accountable institutional subject:

- it MAY own settlement-facing ledger accounts,
- it MAY appear in procurement settlement references,
- it MAY be a target of `procedural/*`, `contract/*`, and `incident/*`
  reputation signals,
- it MUST NOT be admitted into `community/*` reputation signals by default,
- it MUST NOT be treated as a pseudonym, proof-of-personhood substitute, or
  democratic personhood token.

## Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-001 | The canonical v1 organization subject family MUST be `org:did:key:z<base58btc(0xed01 || raw_ed25519_public_key)>`. | Fact | Proposal 017 |
| FR-002 | Parsers and validators MUST treat `org-id:did:key:...` as non-canonical for v1. | Fact | Proposal 017 |
| FR-003 | `reputation-signal.v1` MUST support `subject/kind = org` and require `subject/id` in canonical `org:did:key:...` form when that kind is selected. | Fact | Proposal 017 |
| FR-004 | `procedural/*` reputation signals MAY target `org`. | Fact | Proposal 017 |
| FR-005 | `contract/*` reputation signals MAY target `org`. | Fact | Proposal 017 |
| FR-006 | `incident/*` reputation signals MAY target `org`. | Fact | Proposal 017 |
| FR-007 | `community/*` reputation signals MUST NOT target `org` in the MVP baseline. | Fact | Proposal 017 |
| FR-008 | Settlement-facing account ownership MUST be allowed to bind to `org` without introducing separate procurement-side `kind` fields. | Fact | Proposal 017 + Proposal 016 |
| FR-009 | `payer/account-ref` and `payee/account-ref` in procurement MUST carry subject role inside the canonical identifier prefix rather than through duplicated `payer/kind` or `payee/kind` fields. | Fact | Proposal 017 + Proposal 016 |
| FR-010 | MVP organization custody MUST support at least one `org/custodian-ref` pointing to `participant:did:key:...`. | Fact | Proposal 017 |
| FR-011 | Rollout of `org` MUST preserve the distinction between accountable subjects and pseudonymous subjects; `org` MUST NOT inherit `nym` semantics. | Fact | Proposal 017 |
| FR-012 | `exception-record.v1` MUST admit `org` as an operational owner, requester, and approver subject wherever canonical accountable actors are allowed. | Fact | Proposal 017 |
| FR-013 | Settlement policy artifacts such as `gateway-policy.v1` and `escrow-policy.v1` MUST bind their serving nodes to `operator/org-ref` rather than leaving institutional responsibility implicit. | Fact | Proposal 017 |
| FR-014 | Organization-operated settlement policies MUST support a disclosure/audit artifact that preserves the same `operator/org-ref` during suspensions, incidents, limit changes, or reinstatement events. | Fact | Proposal 017 + Proposal 016 |

## Non-Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| NFR-001 | The identity grammar SHOULD remain regular across subject families, using role-prefixed canonical DID forms rather than mixed naming schemes. | Fact | Proposal 017 |
| NFR-002 | New organization support MUST avoid redundant fields that restate information already present in canonical identifiers. | Fact | Proposal 017 + project values |
| NFR-003 | Organizational accountability rollout MUST remain incremental so that reputation, procurement, and settlement can adopt it without a whole-system rewrite. | Inference | Proposal 017 |
| NFR-004 | Organization support MUST preserve clear audit boundaries between infrastructure (`node`), personhood/service (`participant`), institutions (`org`), and privacy layers (`nym`). | Fact | Proposal 017 |
| NFR-005 | Organization-facing settlement disclosures SHOULD snapshot institutional accountability at event time rather than rely only on dereferencing mutable policy state later. | Fact | Proposal 017 + project values |

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| Organization is forced into `participant` role | Institutional and human accountability collapse into one subject | Introduce explicit `org:did:key` family and preserve role boundaries. |
| `org-id:did:key` and `org:did:key` both circulate | Parser ambiguity and fractured identity space | Freeze one canonical organization family and reject the alternate prefix. |
| Procurement duplicates role in both identifier and `kind` field | Drift and contradictory records | Keep only role-prefixed `account-ref` and forbid duplicate procurement `kind` fields. |
| Organization receives social-layer rumor signals by default | Institutional subjects are treated like pseudonyms | Block `community/* -> org` in MVP. |
| One custodian is mistaken for the whole organization | Misplaced accountability and weak governance | Keep `org` and `org/custodian-ref` semantically distinct. |

## Open Questions

1. Which schema should carry `org/custodian-ref` first: a dedicated organization artifact, settlement account records, or both?
2. What is the minimum threshold-custody extension that does not overfit MVP?
3. Which constitutional-ops document should become the long-term home for organization accountability limits and disclosure rules?
4. Which operational artifact should follow `gateway-policy.v1` and `escrow-policy.v1` in the rollout order: settlement exceptions, gateway audit disclosures, or another governance-facing record?

## Next Actions

1. Introduce `organization-subject.v1` as the canonical artifact carrying `org/custodian-ref`.
2. Add at least one valid `reputation-signal.v1` example targeting `org`.
3. Add one invalid `reputation-signal.v1` example proving that `community/* -> org` is rejected.
4. Extend the next highest-value operational schemas with `org` only where it removes real ambiguity.
