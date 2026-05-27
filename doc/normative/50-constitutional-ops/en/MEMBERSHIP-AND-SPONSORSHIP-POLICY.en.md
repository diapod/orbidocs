# Membership and Sponsorship Policy

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-MEMBERSHIP-SPONSORSHIP-001` |
| `type` | Constitutional operational act / entry and sponsorship policy |
| `version` | `0.2.0-draft` |
| `date` | `2026-05-27` |
| `basis` | Constitution Art. VII, XV, XVI; Core Values; Proposal 051; Procedural Reputation Spec |

## Purpose

This policy defines how participants enter shared Orbiplex influence surfaces without turning membership into a moral purity test.
The question is not "is this person good?" but "which shared surfaces may this subject affect, under which limits, on which evidence, with whose bounded sponsorship, and with what appeal path?".

Orbiplex keeps local reading and local node operation open, while placing sluices around influence.
These sluices protect communication, public memory, marketplace exchange, governance, routing, custody, and public-trust surfaces from Sybil pressure, spam, fraud, factional capture, and careless endorsement.

## Canonical Vocabulary

Membership and surface-access schemas use `doc/schemas/_shared/membership-enums.v1.schema.json` as the shared vocabulary source.
Normative prose may explain those terms, but implementations should not copy enum lists by hand.

The entry classes are:

- `guest`
- `contactable-participant`
- `sponsored-candidate`
- `probationary-member`
- `full-participant`
- `public-trust-role`

The influence surfaces are:

- `local-read`
- `contactability`
- `public-comment`
- `public-publishing`
- `unsolicited-dm`
- `broadcast`
- `marketplace`
- `custody`
- `routing`
- `moderation`
- `arbitration`
- `governance`
- `public-trust`

`public-trust-role` is an entry class.
`public-trust` is the surface where high-stakes role authority is exercised.

## Canonical Access Matrix

There is no single global `accepted` state that unlocks every shared capability.
Entry policy is applied through a matrix of `(entry-class, surface) -> decision`, captured by `surface-access-policy.v1`.

| Entry class | Surface | Default decision | Additional gate |
|---|---|---|---|
| `guest` | `local-read` | `allow` | local software and public reading only |
| `guest` | any shared influence surface | `deny` | no common-surface influence by default |
| `contactable-participant` | `contactability` | `probation+attestation` | contact-channel attestation; anti-spam limits |
| `contactable-participant` | `public-comment` | `review` | community policy may allow low-rate comments |
| `sponsored-candidate` | `public-comment` | `n-sponsors` | one scoped sponsor by default; slow-start limits |
| `sponsored-candidate` | `public-publishing` | `review` | sponsor scope and content-surface policy |
| `probationary-member` | `public-comment` | `allow` | low-rate or normal limits by local policy |
| `probationary-member` | `unsolicited-dm` | `deny` | relationship or opt-in required |
| `probationary-member` | `broadcast` | `deny` | no high fan-out by default |
| `probationary-member` | `marketplace` | `review` | low value cap, escrow/procurement contract |
| `full-participant` | `broadcast` | `review` | reputation, rate limits, and anti-collusion checks |
| `full-participant` | `routing` | `review` | capability passport, reliability history |
| `full-participant` | `custody` | `review` | capability passport, storage policy, audit |
| `full-participant` | `governance` | `review` | procedural reputation and COI checks |
| `public-trust-role` | `public-trust` | `review` | IAL, procedural reputation, COI, audit, revocability |

The matrix is intentionally conservative.
Federations may relax or tighten rows, but they should publish the result as `surface-access-policy.v1` rather than embedding it as hidden runtime branches.

## Sponsorship

Sponsorship is a scoped accountability relation, not a guarantee of moral quality.
A sponsor states:

> I know this subject well enough to introduce it to this Orbiplex surface, within this scope and risk limit, and I accept bounded reputational exposure if the sponsorship was grossly careless or collusive.

Sponsorship gives candidacy, not authority.
A sponsored subject still needs the required attestations, probation, policy checks, and runtime limits for the target surface.

The default sponsorship templates are:

| Template | Meaning | Default use |
|---|---|---|
| `light-vouch` | weak introduction, low exposure | contactability or very low-risk local community entry |
| `standard-introduction` | ordinary scoped sponsorship | basic community entry and low-rate public comment |
| `strong-vouch` | high-confidence scoped sponsorship | broader publishing or marketplace probation |
| `mentor-with-liability` | active mentor relation with stronger accountability | high-touch probation or sensitive community onboarding |

The sponsorship artifact records the template, scopes, issuance and expiry, probation window, structured due-diligence references, revocability, revocation-tail duration, and evidence policy.
It does not carry ad-hoc numeric exposure fields; those are policy projections from the template and evidence.

## Sponsor Liability

Derived sponsor liability is direct by default.
It may attach to the sponsor when evidence shows negligent, reckless, or collusive sponsorship during the fresh sponsorship window.

Liability is classified ordinally, not by multiplying local coefficients:

| Class | Meaning | Typical triggers |
|---|---|---|
| `negligible` | no meaningful derived liability | harm was unforeseeable or unrelated to the sponsorship scope |
| `mitigated` | reduced liability after constructive response | sponsor revoked promptly, reported red flags, or helped contain harm |
| `moderate` | ordinary bounded liability | sponsor missed weak signals or sponsored too broadly for the scope |
| `serious` | strong liability | sponsor ignored repeated red flags, mass-sponsored, or exceeded competence |
| `collusive` | sponsor was part of an abuse pattern | anti-collusion sweep finds sponsor-ring or coordinated capture |

Every classification must include triggered conditions and evidence references.
This makes the decision challengeable without pretending that five local numeric factors are a portable truth.

Liability does not propagate beyond one level unless an anti-collusion process establishes an organized sponsor ring.

## Anti-Clan Controls

Sponsorship must not become a private aristocracy.
Federations and communities should enforce:

- sponsorship only within the sponsor's own scope of reputation and authority,
- independent sponsors for higher-risk surfaces,
- graph-distance or cluster-diversity requirements,
- limits on active sponsorships per period,
- automatic review for abnormal sponsorship velocity,
- one-hop liability by default,
- anti-sponsor-ring detection,
- and appeal rights for both sponsor and sponsored subject.

The MVP baseline detector for sponsorship abuse is **abnormal sponsorship velocity**: too many active sponsorships per sponsor within a policy window, with policy-tunable thresholds.

## Newcomer Slow-Start

New entrants should begin with narrow capability limits.
The canonical defaults are expressed by:

- `default.surface-access-policy.json`
- `newcomer.participant-entry-profile.json`
- `newcomer.participant-effective-limits.json`

Those examples are schema-backed and should be treated as the canonical newcomer profile fixture.
Documents should link to them rather than duplicating YAML blocks.

These are defaults, not permanent exclusion.
Constructive, independently evidenced action should make advancement cheaper than destructive action.

## Sanctions and Return Path

Sanctions are expressed as `(surface x intensity)`, not as one mixed ladder of unrelated actions.

| Surface group | `soft` | `hold` | `hard` | `block` |
|---|---|---|---|---|
| `communication` | rate-limit | DM restriction | routing cut-off | federation block |
| `marketplace` | rate-limit | marketplace hold | escrow-only | marketplace block |
| `reputation` | downweight | quarantine | freeze | revoke projection |
| `role` | warning | review | suspension | revocation |
| `relationship` | warn | sponsor review | sponsor revoke | sponsor-ring action |
| `routing` | deprioritize | require fresh proof | cut-off | federation block |
| `custody` | require review | hold writes | suspend custody | revoke custody eligibility |
| `governance` | reduce weight | recusal | suspend voting/panel eligibility | governance block |

The canonical intensity order is `soft < hold < hard < block`.
Sanctions must preserve an audit trace, appeal path, and repair path unless there is an immediate safety threat.
They should restrict influence surfaces rather than erase personhood.

## Anti-Collusion Baselines

The first implementation should not try to detect every collusion form at once.
The MVP baseline detectors are:

- sponsorship: abnormal sponsorship velocity,
- public adjudication: co-flagging coherence, for example Jaccard similarity of flagger sets across objects,
- marketplace: closed-loop receipt detection, for example settlement cycles such as `A -> B -> C -> A`.

Additional detectors should be added explicitly when there is operational evidence that the baseline is insufficient.

## Related Contracts

This policy is supported by:

- `membership-invitation.v1`
- `membership-sponsorship.v1`
- `membership-acceptance.v1`
- `participant-entry-profile.v1`
- `participant-effective-limits.v1`
- `surface-access-policy.v1`
- `participant-capability-limits.v1`
- `reputation-signal.v1`
