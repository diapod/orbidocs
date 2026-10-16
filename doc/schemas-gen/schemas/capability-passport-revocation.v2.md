# Capability-passport-revocation.v2

Source schema: [`doc/schemas/capability-passport-revocation.v2.schema.json`](../../schemas/capability-passport-revocation.v2.schema.json)

## Governing Basis

- [`doc/project/40-proposals/076-limited-messaging-grants-decision.md`](../../project/40-proposals/076-limited-messaging-grants-decision.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `capability-passport-revocation.v2` |  |
| [`revocation_id`](#field-revocation-id) | `yes` | string |  |
| [`federation_id`](#field-federation-id) | `yes` | string |  |
| [`target_id`](#field-target-id) | `yes` | string |  |
| [`delegation_id`](#field-delegation-id) | `yes` | string |  |
| [`node_id`](#field-node-id) | `yes` | string |  |
| [`revoked_at`](#field-revoked-at) | `yes` | string |  |
| [`signed_by`](#field-signed-by) | `yes` | enum: `authority`, `subject-node` |  |
| [`signatures`](#field-signatures) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-passport-revocation.v2`

<a id="field-revocation-id"></a>
## `revocation_id`

- Required: `yes`
- Shape: string

<a id="field-federation-id"></a>
## `federation_id`

- Required: `yes`
- Shape: string

<a id="field-target-id"></a>
## `target_id`

- Required: `yes`
- Shape: string

<a id="field-delegation-id"></a>
## `delegation_id`

- Required: `yes`
- Shape: string

<a id="field-node-id"></a>
## `node_id`

- Required: `yes`
- Shape: string

<a id="field-revoked-at"></a>
## `revoked_at`

- Required: `yes`
- Shape: string

<a id="field-signed-by"></a>
## `signed_by`

- Required: `yes`
- Shape: enum: `authority`, `subject-node`

<a id="field-signatures"></a>
## `signatures`

- Required: `yes`
- Shape: array
