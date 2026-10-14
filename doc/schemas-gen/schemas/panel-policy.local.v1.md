# Panel-policy.local.v1

Source schema: [`doc/schemas/panel-policy.local.v1.schema.json`](../../schemas/panel-policy.local.v1.schema.json)

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
| [`schema`](#field-schema) | `yes` | const: `panel-policy.local.v1` |  |
| [`id`](#field-id) | `yes` | string |  |
| [`revision`](#field-revision) | `yes` | integer |  |
| [`profile`](#field-profile) | `yes` | const: `local-panel.tai-fixtures.v1` |  |
| [`federation/id`](#field-federation-id) | `yes` | string |  |
| [`min-entry-class`](#field-min-entry-class) | `yes` | enum: `full-participant`, `public-trust-role` |  |
| [`min-ial`](#field-min-ial) | `yes` | integer |  |
| [`critical`](#field-critical) | `yes` | boolean |  |
| [`recipients`](#field-recipients) | `yes` | array |  |
| [`auditors`](#field-auditors) | `yes` | array |  |
| [`input-admitters`](#field-input-admitters) | `yes` | array |  |
| [`heartbeat-owners`](#field-heartbeat-owners) | `yes` | array |  |
| [`coordinators`](#field-coordinators) | `yes` | array |  |
| [`eligibility-owners`](#field-eligibility-owners) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `panel-policy.local.v1`

<a id="field-id"></a>
## `id`

- Required: `yes`
- Shape: string

<a id="field-revision"></a>
## `revision`

- Required: `yes`
- Shape: integer

<a id="field-profile"></a>
## `profile`

- Required: `yes`
- Shape: const: `local-panel.tai-fixtures.v1`

<a id="field-federation-id"></a>
## `federation/id`

- Required: `yes`
- Shape: string

<a id="field-min-entry-class"></a>
## `min-entry-class`

- Required: `yes`
- Shape: enum: `full-participant`, `public-trust-role`

<a id="field-min-ial"></a>
## `min-ial`

- Required: `yes`
- Shape: integer

<a id="field-critical"></a>
## `critical`

- Required: `yes`
- Shape: boolean

<a id="field-recipients"></a>
## `recipients`

- Required: `yes`
- Shape: array

<a id="field-auditors"></a>
## `auditors`

- Required: `yes`
- Shape: array

<a id="field-input-admitters"></a>
## `input-admitters`

- Required: `yes`
- Shape: array

<a id="field-heartbeat-owners"></a>
## `heartbeat-owners`

- Required: `yes`
- Shape: array

<a id="field-coordinators"></a>
## `coordinators`

- Required: `yes`
- Shape: array

<a id="field-eligibility-owners"></a>
## `eligibility-owners`

- Required: `yes`
- Shape: object
