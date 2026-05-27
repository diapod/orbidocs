# Surface Access Policy v1

Source schema: [`doc/schemas/surface-access-policy.v1.schema.json`](../../schemas/surface-access-policy.v1.schema.json)

Policy-as-data matrix for deciding access by entry class and influence surface. This is the canonical policy-axis source of truth; participant entry profiles are computed projections.

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
| [`policy/id`](#field-policy-id) | `yes` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`valid/until`](#field-valid-until) | `no` | string |  |
| [`decision/default`](#field-decision-default) | `yes` | ref: `_shared/membership-enums.v1.schema.json#/$defs/surface_decision` |  |
| [`matrix`](#field-matrix) | `yes` | array |  |
| [`appeal/ref`](#field-appeal-ref) | `no` | string |  |
| [`notes`](#field-notes) | `no` | string |  |
| [`extensions`](#field-extensions) | `no` | ref: `_shared/membership-enums.v1.schema.json#/$defs/extensions` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`matrix_rule`](#def-matrix-rule) | object |  |
| [`default_limit`](#def-default-limit) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-policy-id"></a>
## `policy/id`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid/until`

- Required: `no`
- Shape: string

<a id="field-decision-default"></a>
## `decision/default`

- Required: `yes`
- Shape: ref: `_shared/membership-enums.v1.schema.json#/$defs/surface_decision`

<a id="field-matrix"></a>
## `matrix`

- Required: `yes`
- Shape: array

<a id="field-appeal-ref"></a>
## `appeal/ref`

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

<a id="def-matrix-rule"></a>
## `$defs.matrix_rule`

- Shape: object

<a id="def-default-limit"></a>
## `$defs.default_limit`

- Shape: object
