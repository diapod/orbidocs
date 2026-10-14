# Panel-eligibility-fact.local.v1

Source schema: [`doc/schemas/panel-eligibility-fact.local.v1.schema.json`](../../schemas/panel-eligibility-fact.local.v1.schema.json)

Draft local fixture contract. Shape validation confers no admission, mandate, application receipt or normative ELL2 qualification.

## Governing Basis

- [`doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`](../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md)
- [`doc/normative/50-constitutional-ops/pl/PANEL-SELECTION-PROTOCOL.pl.md`](../../normative/50-constitutional-ops/pl/PANEL-SELECTION-PROTOCOL.pl.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`source`](#field-source) | `yes` | object |  |
| [`owner`](#field-owner) | `yes` | string |  |
| [`subject/id`](#field-subject-id) | `yes` | string |  |
| [`valid-from`](#field-valid-from) | `yes` | string |  |
| [`valid-until`](#field-valid-until) | `yes` | string |  |
| [`synthetic`](#field-synthetic) | `yes` | boolean |  |
| [`method`](#field-method) | `yes` | string |  |
| [`value`](#field-value) | `yes` | unspecified |  |
## Field Semantics

<a id="field-source"></a>
## `source`

- Required: `yes`
- Shape: object

<a id="field-owner"></a>
## `owner`

- Required: `yes`
- Shape: string

<a id="field-subject-id"></a>
## `subject/id`

- Required: `yes`
- Shape: string

<a id="field-valid-from"></a>
## `valid-from`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid-until`

- Required: `yes`
- Shape: string

<a id="field-synthetic"></a>
## `synthetic`

- Required: `yes`
- Shape: boolean

<a id="field-method"></a>
## `method`

- Required: `yes`
- Shape: string

<a id="field-value"></a>
## `value`

- Required: `yes`
- Shape: unspecified
