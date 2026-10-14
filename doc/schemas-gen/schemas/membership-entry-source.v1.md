# Membership-entry-source.v1

Source schema: [`doc/schemas/membership-entry-source.v1.schema.json`](../../schemas/membership-entry-source.v1.schema.json)

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
| [`schema`](#field-schema) | `yes` | const: `membership-entry-source.v1` |  |
| [`source/id`](#field-source-id) | `yes` | string |  |
| [`revision`](#field-revision) | `yes` | integer |  |
| [`issuer/ref`](#field-issuer-ref) | `yes` | string |  |
| [`subject/ref`](#field-subject-ref) | `yes` | string |  |
| [`policy`](#field-policy) | `yes` | object |  |
| [`valid-from`](#field-valid-from) | `yes` | string |  |
| [`valid-until`](#field-valid-until) | `yes` | string |  |
| [`origin`](#field-origin) | `yes` | unspecified |  |
| [`fact`](#field-fact) | `yes` | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `membership-entry-source.v1`

<a id="field-source-id"></a>
## `source/id`

- Required: `yes`
- Shape: string

<a id="field-revision"></a>
## `revision`

- Required: `yes`
- Shape: integer

<a id="field-issuer-ref"></a>
## `issuer/ref`

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

<a id="field-valid-from"></a>
## `valid-from`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid-until`

- Required: `yes`
- Shape: string

<a id="field-origin"></a>
## `origin`

- Required: `yes`
- Shape: unspecified

<a id="field-fact"></a>
## `fact`

- Required: `yes`
- Shape: unspecified
