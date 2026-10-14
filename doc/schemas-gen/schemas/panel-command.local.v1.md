# Panel-command.local.v1

Source schema: [`doc/schemas/panel-command.local.v1.schema.json`](../../schemas/panel-command.local.v1.schema.json)

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
| [`schema`](#field-schema) | `yes` | const: `panel-command.local.v1` |  |
| [`command/id`](#field-command-id) | `yes` | string |  |
| [`actor/id`](#field-actor-id) | `yes` | string |  |
| [`context`](#field-context) | `yes` | object |  |
| [`procedure`](#field-procedure) | `yes` | object |  |
| [`panel-policy`](#field-panel-policy) | `yes` | object |  |
| [`round`](#field-round) | `yes` | integer |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`action`](#field-action) | `yes` | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `panel-command.local.v1`

<a id="field-command-id"></a>
## `command/id`

- Required: `yes`
- Shape: string

<a id="field-actor-id"></a>
## `actor/id`

- Required: `yes`
- Shape: string

<a id="field-context"></a>
## `context`

- Required: `yes`
- Shape: object

<a id="field-procedure"></a>
## `procedure`

- Required: `yes`
- Shape: object

<a id="field-panel-policy"></a>
## `panel-policy`

- Required: `yes`
- Shape: object

<a id="field-round"></a>
## `round`

- Required: `yes`
- Shape: integer

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

<a id="field-action"></a>
## `action`

- Required: `yes`
- Shape: unspecified
