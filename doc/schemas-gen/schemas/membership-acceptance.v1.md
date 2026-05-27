# Membership Acceptance v1

Source schema: [`doc/schemas/membership-acceptance.v1.schema.json`](../../schemas/membership-acceptance.v1.schema.json)

Append-only acceptance fact showing that a subject accepted entry into a bounded Orbiplex policy surface and covenant. Acceptance is not a universal authority grant.

## Governing Basis

- [`P051`](../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md)
- [`Participant Covenant`](../../normative/50-constitutional-ops/en/PARTICIPANT-COVENANT.en.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`acceptance/id`](#field-acceptance-id) | `yes` | string |  |
| [`participant/subject`](#field-participant-subject) | `yes` | ref: `_shared/membership-enums.v1.schema.json#/$defs/subject` |  |
| [`accepted/at`](#field-accepted-at) | `yes` | string |  |
| [`entry/profile`](#field-entry-profile) | `yes` | ref: `_shared/membership-enums.v1.schema.json#/$defs/entry_profile_class` |  |
| [`invitation/ref`](#field-invitation-ref) | `no` | string |  |
| [`sponsorship/refs`](#field-sponsorship-refs) | `no` | array |  |
| [`covenant/ref`](#field-covenant-ref) | `yes` | string |  |
| [`surface-policy/ref`](#field-surface-policy-ref) | `yes` | string |  |
| [`probation/until`](#field-probation-until) | `no` | string |  |
| [`status`](#field-status) | `yes` | enum: `accepted`, `probationary`, `completed`, `withdrawn`, `revoked` |  |
| [`notes`](#field-notes) | `no` | string |  |
| [`extensions`](#field-extensions) | `no` | ref: `_shared/membership-enums.v1.schema.json#/$defs/extensions` |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-acceptance-id"></a>
## `acceptance/id`

- Required: `yes`
- Shape: string

<a id="field-participant-subject"></a>
## `participant/subject`

- Required: `yes`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/subject`

<a id="field-accepted-at"></a>
## `accepted/at`

- Required: `yes`
- Shape: string

<a id="field-entry-profile"></a>
## `entry/profile`

- Required: `yes`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/entry_profile_class`

<a id="field-invitation-ref"></a>
## `invitation/ref`

- Required: `no`
- Shape: string

<a id="field-sponsorship-refs"></a>
## `sponsorship/refs`

- Required: `no`
- Shape: array

<a id="field-covenant-ref"></a>
## `covenant/ref`

- Required: `yes`
- Shape: string

<a id="field-surface-policy-ref"></a>
## `surface-policy/ref`

- Required: `yes`
- Shape: string

<a id="field-probation-until"></a>
## `probation/until`

- Required: `no`
- Shape: string

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `accepted`, `probationary`, `completed`, `withdrawn`, `revoked`

<a id="field-notes"></a>
## `notes`

- Required: `no`
- Shape: string

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/extensions`
