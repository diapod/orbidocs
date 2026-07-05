# Proposal 017: Organization Subjects and `org:did:key`

## Context

The current identity layer distinguishes several canonical role-prefixed subject
families:

- `node:did:key:...`
- `participant:did:key:...`
- `nym:did:key:...`
- `council:did:key:...`

That convention is now stable enough to extend. The new settlement workstream
introduced in Proposal 016 also exposes a practical gap: some procurement, escrow,
gateway, and governance actions may need to attach to a durable organization-level
subject rather than only to an individual participant or an infrastructure node.

The gap is real in at least three places:

1. a gateway or escrow provider may be operated under organizational responsibility,
2. a prepaid ledger account may belong to an organization rather than one person,
3. governance and procedural review may need to target an accountable organization
   without collapsing that organization into a pseudonym or into one employee's
   participant identity.

This proposal formalizes the missing subject family and names its MVP custody model.

## Goals

- add an organization-scoped canonical identifier family that matches the existing
  role-prefixed DID style,
- keep the identity grammar regular instead of introducing ad hoc `*-id:` prefixes,
- distinguish accountable organizations from mere presentation aliases,
- support procurement and settlement use cases without forcing immediate rollout
  across every schema,
- preserve the existing separation between organizational accountability and
  democratic or rumor-level participation.

## Decision

The canonical organization subject family SHALL be:

`org:did:key:z<base58btc(0xed01 || raw_ed25519_public_key)>`

The repository SHOULD treat this as the natural continuation of the existing
role-prefixed identity convention, not as a new naming style. Therefore:

- `org:did:key:...` is canonical,
- `org-id:did:key:...` is rejected as non-canonical for v1,
- organization subjects are accountable entities,
- organization subjects are not mere nyms and MUST NOT inherit nym semantics,
- organization subjects do not automatically gain democratic or whisper-layer rights
  merely by existing.

## Proposed Model

### 1. Identity Family

An organization subject is a durable responsibility anchor representing an
institutional or group actor.

Canonical form:

`org:did:key:...`

Rationale:

- it matches `node`, `participant`, `nym`, and `council`,
- it keeps parsers simple and role-prefixed,
- it avoids a mixed convention where some subject families use `foo:` and others
  use `foo-id:`.

### 2. MVP Custody

For MVP, an organization subject may be administered by one designated custodian.

Semantic minimum:

- `subject/kind = org`
- `subject/id = org:did:key:...`
- `org/custodian-ref = participant:did:key:...`

This is intentionally modest. It gives the system one accountable human-side anchor
for operational actions while leaving room for later threshold or multisig custody.

The custody upgrade path should remain open:

- MVP: one custodian,
- later: multiple custodians with threshold policy,
- later still: policy-bound board, panel, or delegated operating roles.

The smallest planned threshold-custody extension is a simple `k-of-n` custody
policy reference plus signer set. Full governance workflows remain outside the MVP
threshold-custody extension.

### 3. Accountability Scope

Organization subjects MAY be used as:

- owners of supervised ledger accounts,
- counterparties in procurement and settlement flows,
- targets of procedural or contract-domain reputation signals,
- referenced custodians in operational and audit records.

Organization subjects MUST NOT automatically be used as:

- public pseudonyms,
- community-rumor subjects by default,
- democratic voters or proof-of-personhood substitutes,
- anonymity layers.

This preserves a necessary asymmetry:

- `org` is an accountable entity,
- `nym` is a presentation/privacy layer,
- these are not interchangeable.

### 4. Relationship to Existing Identity Layers

The organization layer complements rather than replaces current subjects.

- `node` remains the infrastructure actor,
- `participant` remains the human accountability and service actor,
- `pod-user` remains the hosted-user actor,
- `nym` remains the privacy-preserving authored layer,
- `org` adds a durable institutional accountability layer.

One real-world operator may therefore appear in several roles without semantic
collapse:

- a person acts as `participant:did:key:...`,
- that person may custody `org:did:key:...`,
- a node advertises `node:did:key:...`,
- and a public authored surface may still use `nym:did:key:...`.

### 5. Rollout Boundaries

This proposal does not require an immediate mutation of every schema.

Immediate follow-up candidates:

- supervised ledger account ownership,
- gateway and escrow policy references,
- procurement counterparties where institutional billing matters,
- `reputation-signal.v1` for `procedural/*` and `contract/*` domains.

Deferred for later:

- democratic rights and proof-of-personhood implications,
- org-level anonymity or pseudonymity systems,
- threshold custody schema,
- org-to-org delegation chains.

## Trade-offs

### Benefits

- regular identity grammar,
- explicit organization accountability,
- cleaner procurement and gateway modeling,
- less pressure to overload `participant` or `nym` with institutional semantics.

### Costs

- one more subject family to reason about,
- later schema work across reputation and governance artifacts,
- custody semantics must be documented carefully to avoid false assumptions about
  who actually controls an organization subject.

### Risks

- if organizations are allowed into every domain too early, the model can bloat,
- if organizations are treated as democratic actors too quickly, institutional power
  may overshadow personhood-bound safeguards,
- if custody remains underspecified, the system may confuse one custodian with the
  whole organization.

## Open Questions

No unresolved questions remain for this proposal slice. The decisions below
record the approved defaults.

Resolved 2026-07-05:

1. The first rollout admits `subject/kind = org` only in custody, procurement,
   and governance accountability artifacts. Organization subjects are introduced
   where the organization is an accountable party, not as a blanket replacement
   for participant subjects.
2. Procurement contracts grow explicit `payer/kind` and `payee/kind` fields.
   Account ownership is not the only source of party semantics.
3. The smallest threshold-custody extension is a simple `k-of-n` custody policy
   reference plus signer set. Full governance workflows remain outside the MVP
   threshold-custody extension.
4. Organization accountability limits should move into a dedicated
   constitutional-ops act for Organization Accountability. Role-to-IAL and
   federation quorum documents may reference that act, but should not become the
   primary home for organization accountability semantics.

## Next Actions

1. Extend the subject-family invariants memo to include `org`.
2. Add `org` support to the first settlement-facing schemas that need it.
3. Open a focused requirements document for organization subject custody and schema
   rollout order.
4. Update `reputation-signal.v1` only after the organization subject invariants are
   frozen.
5. Extend procurement contract work to carry explicit `payer/kind` and
   `payee/kind`; account ownership is not enough to express party semantics.
6. Add the minimal `k-of-n` custody policy reference plus signer-set seam to the
   threshold-custody follow-up, without pulling full governance workflows into MVP.
7. Open the constitutional-ops Organization Accountability act as the long-term
   normative home for organization accountability limits.
