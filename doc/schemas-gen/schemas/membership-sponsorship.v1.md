# Membership Sponsorship v1

Source schema: [`doc/schemas/membership-sponsorship.v1.schema.json`](../../schemas/membership-sponsorship.v1.schema.json)

Append-only scoped sponsorship fact. Sponsorship grants candidacy to named surfaces and creates bounded, evidence-backed sponsor exposure; it does not directly grant authority.

## Governing Basis

- [`P051`](../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md)
- [`Membership Policy`](../../normative/50-constitutional-ops/en/MEMBERSHIP-AND-SPONSORSHIP-POLICY.en.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`sponsorship/id`](#field-sponsorship-id) | `yes` | string |  |
| [`sponsor/subject`](#field-sponsor-subject) | `yes` | ref: `_shared/membership-enums.v1.schema.json#/$defs/subject` |  |
| [`invitee/subject`](#field-invitee-subject) | `yes` | ref: `_shared/membership-enums.v1.schema.json#/$defs/subject` |  |
| [`scopes`](#field-scopes) | `yes` | ref: `_shared/membership-enums.v1.schema.json#/$defs/scopes` |  |
| [`sponsorship/template`](#field-sponsorship-template) | `yes` | ref: `_shared/membership-enums.v1.schema.json#/$defs/sponsorship_template` |  |
| [`liability/class`](#field-liability-class) | `no` | ref: `_shared/membership-enums.v1.schema.json#/$defs/sponsor_liability_class` |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`probation/until`](#field-probation-until) | `yes` | string |  |
| [`due-diligence/refs`](#field-due-diligence-refs) | `yes` | array |  |
| [`revocable`](#field-revocable) | `yes` | boolean |  |
| [`revoked/at`](#field-revoked-at) | `no` | string |  |
| [`revocation-tail-duration`](#field-revocation-tail-duration) | `yes` | ref: `_shared/membership-enums.v1.schema.json#/$defs/iso8601_duration` |  |
| [`evidence/policy`](#field-evidence-policy) | `yes` | ref: `_shared/membership-enums.v1.schema.json#/$defs/evidence_policy` |  |
| [`policy/ref`](#field-policy-ref) | `no` | string |  |
| [`notes`](#field-notes) | `no` | string |  |
| [`extensions`](#field-extensions) | `no` | ref: `_shared/membership-enums.v1.schema.json#/$defs/extensions` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`due_diligence_ref`](#def-due-diligence-ref) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-sponsorship-id"></a>
## `sponsorship/id`

- Required: `yes`
- Shape: string

<a id="field-sponsor-subject"></a>
## `sponsor/subject`

- Required: `yes`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/subject`

<a id="field-invitee-subject"></a>
## `invitee/subject`

- Required: `yes`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/subject`

<a id="field-scopes"></a>
## `scopes`

- Required: `yes`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/scopes`

<a id="field-sponsorship-template"></a>
## `sponsorship/template`

- Required: `yes`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/sponsorship_template`

<a id="field-liability-class"></a>
## `liability/class`

- Required: `no`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/sponsor_liability_class`

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-probation-until"></a>
## `probation/until`

- Required: `yes`
- Shape: string

<a id="field-due-diligence-refs"></a>
## `due-diligence/refs`

- Required: `yes`
- Shape: array

<a id="field-revocable"></a>
## `revocable`

- Required: `yes`
- Shape: boolean

<a id="field-revoked-at"></a>
## `revoked/at`

- Required: `no`
- Shape: string

<a id="field-revocation-tail-duration"></a>
## `revocation-tail-duration`

- Required: `yes`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/iso8601_duration`

<a id="field-evidence-policy"></a>
## `evidence/policy`

- Required: `yes`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/evidence_policy`

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `no`
- Shape: string

<a id="field-notes"></a>
## `notes`

- Required: `no`
- Shape: string

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/extensions`

## Definition Semantics

<a id="def-due-diligence-ref"></a>
## `$defs.due_diligence_ref`

- Shape: object
