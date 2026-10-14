# Membership-admission-policy.v1

Source schema: [`doc/schemas/membership-admission-policy.v1.schema.json`](../../schemas/membership-admission-policy.v1.schema.json)

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
| [`schema`](#field-schema) | `yes` | const: `membership-admission-policy.v1` |  |
| [`policy/id`](#field-policy-id) | `yes` | string |  |
| [`revision`](#field-revision) | `yes` | integer |  |
| [`host/id`](#field-host-id) | `yes` | string |  |
| [`test-subjects`](#field-test-subjects) | `yes` | array |  |
| [`issuers`](#field-issuers) | `yes` | object |  |
| [`admitters`](#field-admitters) | `yes` | array |  |
| [`surface-policy`](#field-surface-policy) | `yes` | ref: `surface-access-policy.v1.schema.json` |  |
| [`controllers`](#field-controllers) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `membership-admission-policy.v1`

<a id="field-policy-id"></a>
## `policy/id`

- Required: `yes`
- Shape: string

<a id="field-revision"></a>
## `revision`

- Required: `yes`
- Shape: integer

<a id="field-host-id"></a>
## `host/id`

- Required: `yes`
- Shape: string

<a id="field-test-subjects"></a>
## `test-subjects`

- Required: `yes`
- Shape: array

<a id="field-issuers"></a>
## `issuers`

- Required: `yes`
- Shape: object

<a id="field-admitters"></a>
## `admitters`

- Required: `yes`
- Shape: array

<a id="field-surface-policy"></a>
## `surface-policy`

- Required: `yes`
- Shape: ref: `surface-access-policy.v1.schema.json`

<a id="field-controllers"></a>
## `controllers`

- Required: `yes`
- Shape: object
