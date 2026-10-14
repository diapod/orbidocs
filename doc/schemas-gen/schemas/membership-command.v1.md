# Membership-command.v1

Source schema: [`doc/schemas/membership-command.v1.schema.json`](../../schemas/membership-command.v1.schema.json)

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
| [`schema`](#field-schema) | `yes` | const: `membership-command.v1` |  |
| [`command/id`](#field-command-id) | `yes` | string |  |
| [`host/id`](#field-host-id) | `yes` | string |  |
| [`host/incarnation`](#field-host-incarnation) | `yes` | string |  |
| [`actor/id`](#field-actor-id) | `yes` | string |  |
| [`subject/ref`](#field-subject-ref) | `yes` | string |  |
| [`policy`](#field-policy) | `yes` | object |  |
| [`expected-revision`](#field-expected-revision) | `yes` | integer |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`action`](#field-action) | `yes` | unspecified |  |
| [`expected-digest`](#field-expected-digest) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `membership-command.v1`

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

<a id="field-subject-ref"></a>
## `subject/ref`

- Required: `yes`
- Shape: string

<a id="field-policy"></a>
## `policy`

- Required: `yes`
- Shape: object

<a id="field-expected-revision"></a>
## `expected-revision`

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

<a id="field-expected-digest"></a>
## `expected-digest`

- Required: `yes`
- Shape: string
