# Requirements 015: Newcomer Influence-Surface Limits

Based on:
- `doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`
- `doc/project/50-requirements/requirements-009-capability-limits.md`
- `doc/project/40-proposals/061-contact-attestation-service.md`
- `doc/project/10-challenges/002-sybil.md`
- `doc/normative/50-constitutional-ops/en/MEMBERSHIP-AND-SPONSORSHIP-POLICY.en.md`
- `doc/normative/50-constitutional-ops/en/PARTICIPANT-COVENANT.en.md`
- `doc/normative/50-constitutional-ops/en/ADVOCACY-AND-SOLICITATION-POLICY.en.md`
- `doc/normative/50-constitutional-ops/en/MARKETPLACE-ANTI-FRAUD-POLICY.en.md`

Date: `2026-05-27`
Status: Draft (implementation-facing policy requirements)

## Executive Summary

This document defines the first implementation-facing requirements for the
default newcomer profile and per-surface influence limits.

The goal is not to decide whether a person is "good enough" to enter Orbiplex.
The goal is to keep shared influence surfaces slow-start, evidence-backed,
revocable, and auditable until the participant has enough independent history.

The implementation baseline is:

- no global binary membership switch,
- explicit surface classes,
- contact attestation as anti-spam/contactability only,
- sponsorship as scoped candidacy, not authority,
- default newcomer limits mapped to policy artifacts,
- and escalation to `participant-capability-limits.v1` when a participant is
  restricted by an explicit sanction.

## Proposed Model / Decision

### Surface Classes

The first policy surface registry is the `surface_id` definition in
`doc/schemas/_shared/membership-enums.v1.schema.json`.
Documentation may explain the list, but implementations MUST consume the shared
definition rather than maintaining another inline enum.

Each surface has its own eligibility threshold.
No implementation should treat contact attestation, sponsorship, or IAL as a
universal unlock.

### Default Newcomer Profile

The default newcomer profile is not repeated here as YAML.
The schema-backed canonical fixtures are:

- `doc/schemas/examples/default.surface-access-policy.json`
- `doc/schemas/examples/newcomer.participant-entry-profile.json`
- `doc/schemas/examples/newcomer.participant-effective-limits.json`

The profile is a starting read model, not an append-only source of truth.
It may be derived from `membership-acceptance.v1`,
`membership-sponsorship.v1`, contact attestation facts, reputation events, and
local policy.

### Policy Axis and Read Models

`surface-access-policy.v1` is the policy-axis source of truth.
It defines a matrix of `(entry-class, surface) -> decision` plus required
attestations, sponsors, reputation gates, and default limits.

`participant-entry-profile.v1` is a computed subject read model.
It identifies the subject's current entry class and provenance, but does not
carry independent per-surface permission truth.

`participant-effective-limits.v1` is the runtime-facing composed read model.
It merges entry defaults, surface policy, capability sanctions, and appeal
results.
The composition rule for MVP is `sanction-overrides-entry-defaults`.

### Relation to `participant-capability-limits.v1`

Newcomer limits are entry policy.
`participant-capability-limits.v1` is sanction or restriction state.

They share operation names and runtime hooks through an effective-limits
projection:

- newcomer limits answer: "what has not yet been earned?"
- capability limits answer: "what has been explicitly restricted?"
- effective limits answer: "what can the runtime do now, after all overlays?"

### Capability-Limit Operation Mapping

| Newcomer/effective-limit operation | Runtime/capability-limit operation | Default newcomer posture |
|---|---|---|
| `public-posting` | `public-posting` | `limited: low-rate` |
| `unsolicited-dm` | `unsolicited-dm` | `deny` |
| `broadcast` | `broadcast` | `deny` |
| `marketplace-value-cap` | `marketplace-value-cap` | `limited: very-low` |
| `links-to-unknown-users` | `links-to-unknown-users` | `limited` |
| `reputation-weight-outgoing` | `reputation-weight-outgoing` | `limited: low` |
| `governance` | `governance` | `deny` |
| `panel-eligibility` | `panel-eligibility` | `deny` |
| `public-trust` | `public-trust` | `deny` |
| `training-ingestion` | `training-ingestion` | `limited: quarantine-by-default` |

## Functional Requirements

| ID | Requirement | Type | Source | Status |
|---|---|---|---|---|
| FR-001 | The system MUST model entry and influence as per-surface eligibility, not as one global participant admission bit. | Fact | P051 + Membership Policy | proposed |
| FR-002 | The policy layer MUST distinguish `guest`, `contactable-participant`, `sponsored-candidate`, `probationary-member`, `full-participant`, and `public-trust-role`. | Fact | Membership Policy | proposed |
| FR-003 | Contact attestation MUST NOT be treated as civil identity or as eligibility for public-trust roles. | Fact | P061 | proposed |
| FR-004 | Sponsorship MUST create scoped candidacy only; it MUST NOT directly grant the sponsored subject authority on the target surface. | Fact | P051 + Membership Policy | proposed |
| FR-005 | A `membership-sponsorship.v1` fact MUST carry sponsor subject, invitee subject, scopes, sponsorship template, issued/expiry timestamps, probation window, structured due-diligence refs, revocability, revocation-tail duration, and evidence policy. | Fact | P051 + Membership Policy | proposed |
| FR-006 | The default newcomer effective limits MUST deny unsolicited DM, deny broadcast, set marketplace value cap to very low, remove governance eligibility, remove panel eligibility, and deny the `public-trust` surface. | Fact | Membership Policy | proposed |
| FR-007 | Newcomer public posting SHOULD be low-rate rather than fully denied where community policy allows public comments. | Inference | P051 + Advocacy Policy | proposed |
| FR-008 | Marketplace access for newcomers MUST be constrained by value caps, escrow/procurement contracts, and a ban on unsolicited financial offers. | Fact | Marketplace Anti-Fraud Policy | proposed |
| FR-009 | Political, ideological, religious, campaign, and commercial persuasion MUST require explicit opt-in surfaces before high fan-out distribution is allowed. | Fact | Advocacy Policy | proposed |
| FR-010 | Higher-risk surfaces SHOULD require multiple sponsors with diversity or graph-distance constraints. | Fact | Membership Policy | proposed |
| FR-011 | Sponsor-derived reputation impact MUST be evidence-backed, capped, challengeable, and one-hop by default outside proven sponsor rings. | Fact | Membership Policy | proposed |
| FR-012 | The runtime SHOULD expose a `participant-entry-profile.v1` read model for UI and policy diagnostics. | Inference | Implementation need | proposed |
| FR-013 | The runtime SHOULD expose or consume `surface-access-policy.v1` as the policy-axis source of truth and project `participant-effective-limits.v1` for enforcement. | Inference | Project architecture | proposed |
| FR-014 | Newcomer limits MUST preserve protected floors for appeal, minimal communication, UBC claims, and dispute paths where the corresponding constitutional policy requires them. | Fact | Requirements 009 + Node Rights Card | proposed |
| FR-015 | Anti-collusion MVP baselines SHOULD include abnormal sponsorship velocity, public co-flagging coherence, and marketplace closed-loop receipt detection. | Fact | P051 + Sybil Challenge | proposed |

## Non-Functional Requirements

| ID | Requirement | Type | Source | Status |
|---|---|---|---|---|
| NFR-001 | Entry policy MUST be auditable as data or append-only facts rather than implicit operator folklore. | Inference | Project values | proposed |
| NFR-002 | Entry policy MUST avoid language that claims to detect morality or inner intent. | Fact | Membership Policy | proposed |
| NFR-003 | Surface limits SHOULD be reversible and reviewable. | Fact | Constitution Art. XVI | proposed |
| NFR-004 | Surface limits SHOULD not create a permanent caste; advancement should be possible through independent, evidence-backed interaction history. | Fact | Membership Policy | proposed |
| NFR-005 | UI and diagnostics SHOULD explain whether a denial is caused by entry profile, capability sanction, missing attestation, missing sponsor diversity, or anti-collusion review. | Inference | Operator usability | proposed |

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| Contact attestation is mistaken for identity or trust | Phone/email verification becomes fake authority | State explicitly that contact attestation unlocks only contactability/anti-spam surfaces. |
| Sponsorship becomes clan gating | Social capital turns into an aristocracy | Require scoped authority, sponsor diversity, sponsorship caps, and anti-sponsor-ring sweep. |
| Newcomer limits become permanent caste | Constructive participants cannot advance | Require probation expiry, independent interactions, source diversity, and appeal/review. |
| Policy is coded as hidden branches | Federations cannot audit or adapt it | Model thresholds as `surface-access-policy.v1` and profiles as `participant-entry-profile.v1`. |
| Marketplace reputation is inflated by self-dealing | Fraud unlocks higher value caps | Require settled first-hand receipts and source diversity; downrank closed-loop receipts. |
| Advocacy policy becomes worldview censorship | Ordinary pluralism is suppressed | Regulate opt-in surface use and disclosure, not belief content itself. |

## Resolved MVP Questions

1. `surface-access-policy.v1` is the policy-axis source of truth.
2. `participant-entry-profile.v1` is a computed subject read model.
3. `participant-effective-limits.v1` is the composed runtime read model and may share hooks with `participant-capability-limits.v1`.
4. The first standardized operations are listed in the capability-limit operation mapping table above.
5. The first anti-sponsor-ring metric is abnormal sponsorship velocity.

## Open Questions

1. Which runtime service should own the first `participant-entry-profile.v1` and `participant-effective-limits.v1` read models?
2. Should communities publish default `surface-access-policy.v1` artifacts through Agora as signed policy records?
3. Which protected-floor operations need explicit non-deniable minimum access before the first runtime implementation?

## Next Actions

1. Freeze schemas for `membership-invitation.v1`, `membership-sponsorship.v1`, `membership-acceptance.v1`, `participant-entry-profile.v1`, `participant-effective-limits.v1`, and `surface-access-policy.v1`.
2. Add examples for a sponsored candidate, a probationary newcomer profile, a default effective limits projection, and a high-risk surface requiring sponsor diversity.
3. Add a first Node read model for local participant entry profile once membership onboarding is implemented.
4. Reuse existing capability-limit runtime hooks where operation names overlap, but keep entry policy distinct from sanctions.
