# Participant Entry Profile v1

Source schema: [`doc/schemas/participant-entry-profile.v1.schema.json`](../../schemas/participant-entry-profile.v1.schema.json)

Computed subject read model describing a participant's current entry class and provenance. It carries no independent per-surface authority; effective limits are projected separately.

## Governing Basis

- [`R015`](../../project/50-requirements/requirements-015-newcomer-surface-limits.md)
- [`Membership Policy`](../../normative/50-constitutional-ops/en/MEMBERSHIP-AND-SPONSORSHIP-POLICY.en.md)

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
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`profile/id`](#field-profile-id) | `yes` | string |  |
| [`subject/ref`](#field-subject-ref) | `yes` | ref: `_shared/membership-enums.v1.schema.json#/$defs/subject` |  |
| [`profile/class`](#field-profile-class) | `yes` | ref: `_shared/membership-enums.v1.schema.json#/$defs/entry_profile_class` |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`valid/until`](#field-valid-until) | `no` | string |  |
| [`probation/until`](#field-probation-until) | `no` | string |  |
| [`required/independent-interactions`](#field-required-independent-interactions) | `no` | integer |  |
| [`required/source-diversity`](#field-required-source-diversity) | `no` | integer |  |
| [`basis/refs`](#field-basis-refs) | `yes` | ref: `#/$defs/ref_list` |  |
| [`applicable-policy/refs`](#field-applicable-policy-refs) | `yes` | ref: `#/$defs/ref_list` |  |
| [`sponsorship/refs`](#field-sponsorship-refs) | `no` | ref: `#/$defs/ref_list` |  |
| [`sanction/refs`](#field-sanction-refs) | `no` | ref: `#/$defs/ref_list` |  |
| [`effective-limits/ref`](#field-effective-limits-ref) | `yes` | string |  |
| [`notes`](#field-notes) | `no` | string |  |
| [`extensions`](#field-extensions) | `no` | ref: `_shared/membership-enums.v1.schema.json#/$defs/extensions` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref_list`](#def-ref-list) | array |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-profile-id"></a>
## `profile/id`

- Required: `yes`
- Shape: string

<a id="field-subject-ref"></a>
## `subject/ref`

- Required: `yes`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/subject`

<a id="field-profile-class"></a>
## `profile/class`

- Required: `yes`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/entry_profile_class`

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid/until`

- Required: `no`
- Shape: string

<a id="field-probation-until"></a>
## `probation/until`

- Required: `no`
- Shape: string

<a id="field-required-independent-interactions"></a>
## `required/independent-interactions`

- Required: `no`
- Shape: integer

<a id="field-required-source-diversity"></a>
## `required/source-diversity`

- Required: `no`
- Shape: integer

<a id="field-basis-refs"></a>
## `basis/refs`

- Required: `yes`
- Shape: ref: `#/$defs/ref_list`

<a id="field-applicable-policy-refs"></a>
## `applicable-policy/refs`

- Required: `yes`
- Shape: ref: `#/$defs/ref_list`

<a id="field-sponsorship-refs"></a>
## `sponsorship/refs`

- Required: `no`
- Shape: ref: `#/$defs/ref_list`

<a id="field-sanction-refs"></a>
## `sanction/refs`

- Required: `no`
- Shape: ref: `#/$defs/ref_list`

<a id="field-effective-limits-ref"></a>
## `effective-limits/ref`

- Required: `yes`
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

<a id="def-ref-list"></a>
## `$defs.ref_list`

- Shape: array
