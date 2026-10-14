# Panel-input-command.local.v1

Source schema: [`doc/schemas/panel-input-command.local.v1.schema.json`](../../schemas/panel-input-command.local.v1.schema.json)

Explicit synthetic local candidate input. Signature and publication do not grant admission; host binding, input owner, test allowlist and CAS remain mandatory.

## Governing Basis

- [`doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`](../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `panel-input-command.local.v1` |  |
| [`command/id`](#field-command-id) | `yes` | string |  |
| [`host/id`](#field-host-id) | `yes` | string |  |
| [`host/incarnation`](#field-host-incarnation) | `yes` | string |  |
| [`actor/id`](#field-actor-id) | `yes` | string |  |
| [`panel-policy`](#field-panel-policy) | `yes` | object |  |
| [`expected-revision`](#field-expected-revision) | `yes` | integer |  |
| [`expected-digest`](#field-expected-digest) | `yes` | string |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`action`](#field-action) | `yes` | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `panel-input-command.local.v1`

<a id="field-command-id"></a>
## `command/id`

- Required: `yes`
- Shape: string

<a id="field-host-id"></a>
## `host/id`

- Required: `yes`
- Shape: string

<a id="field-host-incarnation"></a>
## `host/incarnation`

- Required: `yes`
- Shape: string

<a id="field-actor-id"></a>
## `actor/id`

- Required: `yes`
- Shape: string

<a id="field-panel-policy"></a>
## `panel-policy`

- Required: `yes`
- Shape: object

<a id="field-expected-revision"></a>
## `expected-revision`

- Required: `yes`
- Shape: integer

<a id="field-expected-digest"></a>
## `expected-digest`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

<a id="field-action"></a>
## `action`

- Required: `yes`
- Shape: unspecified
