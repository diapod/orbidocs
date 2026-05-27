# Participant Effective Limits v1

Source schema: [`doc/schemas/participant-effective-limits.v1.schema.json`](../../schemas/participant-effective-limits.v1.schema.json)

Computed read model for runtime-facing per-surface limits after composing entry policy, surface policy, capability sanctions, and appeal results.

## Governing Basis

- [`R015`](../../project/50-requirements/requirements-015-newcomer-surface-limits.md)
- [`Membership Policy`](../../normative/50-constitutional-ops/en/MEMBERSHIP-AND-SPONSORSHIP-POLICY.en.md)
- [`R009`](../../project/50-requirements/requirements-009-capability-limits.md)

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
| [`limits/id`](#field-limits-id) | `yes` | string |  |
| [`subject/ref`](#field-subject-ref) | `yes` | ref: `_shared/membership-enums.v1.schema.json#/$defs/subject` |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`valid/until`](#field-valid-until) | `no` | string |  |
| [`source`](#field-source) | `yes` | array |  |
| [`composition/rule`](#field-composition-rule) | `yes` | enum: `sanction-overrides-entry-defaults` |  |
| [`operations`](#field-operations) | `yes` | array |  |
| [`notes`](#field-notes) | `no` | string |  |
| [`extensions`](#field-extensions) | `no` | ref: `_shared/membership-enums.v1.schema.json#/$defs/extensions` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`source_ref`](#def-source-ref) | object |  |
| [`operation_limit`](#def-operation-limit) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-limits-id"></a>
## `limits/id`

- Required: `yes`
- Shape: string

<a id="field-subject-ref"></a>
## `subject/ref`

- Required: `yes`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/subject`

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid/until`

- Required: `no`
- Shape: string

<a id="field-source"></a>
## `source`

- Required: `yes`
- Shape: array

<a id="field-composition-rule"></a>
## `composition/rule`

- Required: `yes`
- Shape: enum: `sanction-overrides-entry-defaults`

<a id="field-operations"></a>
## `operations`

- Required: `yes`
- Shape: array

<a id="field-notes"></a>
## `notes`

- Required: `no`
- Shape: string

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/extensions`

## Definition Semantics

<a id="def-source-ref"></a>
## `$defs.source_ref`

- Shape: object

<a id="def-operation-limit"></a>
## `$defs.operation_limit`

- Shape: object
