# Participant-restriction-lifecycle-request.v2

Source schema: [`doc/schemas/participant-restriction-lifecycle-request.v2.schema.json`](../../schemas/participant-restriction-lifecycle-request.v2.schema.json)

Draft local contract. Shape validation confers no admission, mandate, application receipt or lifecycle readiness.

## Governing Basis

- [`doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`](../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md)
- [`doc/project/60-solutions/040-capability-limited-restrictions/040-capability-limited-restrictions.md`](../../project/60-solutions/040-capability-limited-restrictions/040-capability-limited-restrictions.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `participant-restriction-lifecycle-request.v2` |  |
| [`request/id`](#field-request-id) | `yes` | string |  |
| [`host/id`](#field-host-id) | `yes` | string |  |
| [`host/incarnation`](#field-host-incarnation) | `yes` | string |  |
| [`source/id`](#field-source-id) | `yes` | string |  |
| [`predecessor`](#field-predecessor) | `yes` | ref: `responsibility-common.v1.schema.json#/$defs/Binding` |  |
| [`action`](#field-action) | `yes` | unspecified |  |
| [`authority`](#field-authority) | `yes` | object |  |
| [`requested-at`](#field-requested-at) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `participant-restriction-lifecycle-request.v2`

<a id="field-request-id"></a>
## `request/id`

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

<a id="field-source-id"></a>
## `source/id`

- Required: `yes`
- Shape: string

<a id="field-predecessor"></a>
## `predecessor`

- Required: `yes`
- Shape: ref: `responsibility-common.v1.schema.json#/$defs/Binding`

<a id="field-action"></a>
## `action`

- Required: `yes`
- Shape: unspecified

<a id="field-authority"></a>
## `authority`

- Required: `yes`
- Shape: object

<a id="field-requested-at"></a>
## `requested-at`

- Required: `yes`
- Shape: string
