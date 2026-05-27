# Membership Shared Enums v1

Source schema: [`doc/schemas/_shared/membership-enums.v1.schema.json`](../../schemas/_shared/membership-enums.v1.schema.json)

Shared vocabulary definitions for membership, sponsorship, newcomer surface limits, and public adjudication contracts.

## Governing Basis

- [`P051`](../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md)
- [`Membership Policy`](../../normative/50-constitutional-ops/en/MEMBERSHIP-AND-SPONSORSHIP-POLICY.en.md)
- [`R015`](../../project/50-requirements/requirements-015-newcomer-surface-limits.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)
- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-009-capability-limits.md`](../../project/50-requirements/requirements-009-capability-limits.md)
- [`doc/project/50-requirements/requirements-015-newcomer-surface-limits.md`](../../project/50-requirements/requirements-015-newcomer-surface-limits.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`subject`](#def-subject) | string | Orbiplex subject reference eligible for membership and sponsorship policy. |
| [`entry_profile_class`](#def-entry-profile-class) | enum: `guest`, `contactable-participant`, `sponsored-candidate`, `probationary-member`, `full-participant`, `public-trust-role` | Entry class used by membership policy. `public-trust-role` remains an entry class for high-stakes eligibility, not a surface id. |
| [`surface_id`](#def-surface-id) | enum: `local-read`, `contactability`, `public-comment`, `public-publishing`, `unsolicited-dm`, `broadcast`, `marketplace`, `custody`, `routing`, `moderation`, `arbitration`, `governance`, `public-trust` | Influence surface id. The public-trust surface is named `public-trust` to avoid colliding with the `public-trust-role` entry class. |
| [`surface_decision`](#def-surface-decision) | enum: `allow`, `deny`, `review`, `n-sponsors`, `probation+attestation` | Canonical matrix cell decision for an entry-class x surface rule. |
| [`sanction_intensity`](#def-sanction-intensity) | enum: `soft`, `hold`, `hard`, `block` | Shared sanction intensity axis. Policies may order it as soft < hold < hard < block. |
| [`sanction_surface`](#def-sanction-surface) | enum: `communication`, `marketplace`, `reputation`, `role`, `relationship`, `routing`, `custody`, `governance` | Surface group used when expressing sanctions as surface x intensity instead of a single ladder. |
| [`evidence_policy`](#def-evidence-policy) | enum: `evidence-backed-only`, `community-policy`, `manual-review` | Policy for evidence required before membership, sponsorship, or liability effects become actionable. |
| [`sponsorship_template`](#def-sponsorship-template) | enum: `light-vouch`, `standard-introduction`, `strong-vouch`, `mentor-with-liability` | Named sponsorship template. Templates avoid false precision from ad-hoc numeric exposure parameters. |
| [`sponsor_liability_class`](#def-sponsor-liability-class) | enum: `negligible`, `mitigated`, `moderate`, `serious`, `collusive` | Ordinal sponsor liability classification derived from trigger evidence. |
| [`due_diligence_kind`](#def-due-diligence-kind) | enum: `known-in-person`, `worked-together`, `verified-credential`, `community-vouch`, `shared-org-membership`, `other-documented` | Structured due-diligence basis for a sponsorship fact. |
| [`adjudication_lifecycle`](#def-adjudication-lifecycle) | enum: `clear`, `under-review`, `judged`, `withdrawn` | Primary lifecycle axis for public object adjudication. |
| [`judgment_qualifier`](#def-judgment-qualifier) | enum: `contested`, `subjective`, `substantiated`, `contaminated` | Judgment qualifier axis meaningful for under-review and judged states. |
| [`limit_operation`](#def-limit-operation) | enum: `public-posting`, `unsolicited-dm`, `broadcast`, `marketplace-value-cap`, `links-to-unknown-users`, `reputation-weight-outgoing`, `governance`, `panel-eligibility`, `public-trust`, `training-ingestion` | Operation names shared by entry-policy effective limits and capability-limit runtime hooks. |
| [`limit_decision`](#def-limit-decision) | enum: `allow`, `deny`, `limited`, `review` | Effective runtime limit decision for one operation on one surface. |
| [`scope`](#def-scope) | string | Dotted policy scope such as `community.basic` or `public-comment.low-volume`. |
| [`scopes`](#def-scopes) | array |  |
| [`iso8601_duration`](#def-iso8601-duration) | string | ISO 8601 duration. Community policy, not schema, sets upper bounds. |
| [`extensions`](#def-extensions) | object | Explicit extension namespace. Consumers MUST NOT treat extension fields as authority unless local policy recognizes them. |
## Field Semantics

## Definition Semantics

<a id="def-subject"></a>
## `$defs.subject`

- Shape: string

Orbiplex subject reference eligible for membership and sponsorship policy.

<a id="def-entry-profile-class"></a>
## `$defs.entry_profile_class`

- Shape: enum: `guest`, `contactable-participant`, `sponsored-candidate`, `probationary-member`, `full-participant`, `public-trust-role`

Entry class used by membership policy. `public-trust-role` remains an entry class for high-stakes eligibility, not a surface id.

<a id="def-surface-id"></a>
## `$defs.surface_id`

- Shape: enum: `local-read`, `contactability`, `public-comment`, `public-publishing`, `unsolicited-dm`, `broadcast`, `marketplace`, `custody`, `routing`, `moderation`, `arbitration`, `governance`, `public-trust`

Influence surface id. The public-trust surface is named `public-trust` to avoid colliding with the `public-trust-role` entry class.

<a id="def-surface-decision"></a>
## `$defs.surface_decision`

- Shape: enum: `allow`, `deny`, `review`, `n-sponsors`, `probation+attestation`

Canonical matrix cell decision for an entry-class x surface rule.

<a id="def-sanction-intensity"></a>
## `$defs.sanction_intensity`

- Shape: enum: `soft`, `hold`, `hard`, `block`

Shared sanction intensity axis. Policies may order it as soft < hold < hard < block.

<a id="def-sanction-surface"></a>
## `$defs.sanction_surface`

- Shape: enum: `communication`, `marketplace`, `reputation`, `role`, `relationship`, `routing`, `custody`, `governance`

Surface group used when expressing sanctions as surface x intensity instead of a single ladder.

<a id="def-evidence-policy"></a>
## `$defs.evidence_policy`

- Shape: enum: `evidence-backed-only`, `community-policy`, `manual-review`

Policy for evidence required before membership, sponsorship, or liability effects become actionable.

<a id="def-sponsorship-template"></a>
## `$defs.sponsorship_template`

- Shape: enum: `light-vouch`, `standard-introduction`, `strong-vouch`, `mentor-with-liability`

Named sponsorship template. Templates avoid false precision from ad-hoc numeric exposure parameters.

<a id="def-sponsor-liability-class"></a>
## `$defs.sponsor_liability_class`

- Shape: enum: `negligible`, `mitigated`, `moderate`, `serious`, `collusive`

Ordinal sponsor liability classification derived from trigger evidence.

<a id="def-due-diligence-kind"></a>
## `$defs.due_diligence_kind`

- Shape: enum: `known-in-person`, `worked-together`, `verified-credential`, `community-vouch`, `shared-org-membership`, `other-documented`

Structured due-diligence basis for a sponsorship fact.

<a id="def-adjudication-lifecycle"></a>
## `$defs.adjudication_lifecycle`

- Shape: enum: `clear`, `under-review`, `judged`, `withdrawn`

Primary lifecycle axis for public object adjudication.

<a id="def-judgment-qualifier"></a>
## `$defs.judgment_qualifier`

- Shape: enum: `contested`, `subjective`, `substantiated`, `contaminated`

Judgment qualifier axis meaningful for under-review and judged states.

<a id="def-limit-operation"></a>
## `$defs.limit_operation`

- Shape: enum: `public-posting`, `unsolicited-dm`, `broadcast`, `marketplace-value-cap`, `links-to-unknown-users`, `reputation-weight-outgoing`, `governance`, `panel-eligibility`, `public-trust`, `training-ingestion`

Operation names shared by entry-policy effective limits and capability-limit runtime hooks.

<a id="def-limit-decision"></a>
## `$defs.limit_decision`

- Shape: enum: `allow`, `deny`, `limited`, `review`

Effective runtime limit decision for one operation on one surface.

<a id="def-scope"></a>
## `$defs.scope`

- Shape: string

Dotted policy scope such as `community.basic` or `public-comment.low-volume`.

<a id="def-scopes"></a>
## `$defs.scopes`

- Shape: array

<a id="def-iso8601-duration"></a>
## `$defs.iso8601_duration`

- Shape: string

ISO 8601 duration. Community policy, not schema, sets upper bounds.

<a id="def-extensions"></a>
## `$defs.extensions`

- Shape: object

Explicit extension namespace. Consumers MUST NOT treat extension fields as authority unless local policy recognizes them.
