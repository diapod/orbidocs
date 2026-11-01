# Witness-key-delegation.v1

Source schema: [`doc/schemas/witness-key-delegation.v1.schema.json`](../../schemas/witness-key-delegation.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `witness-key-delegation.v1` |  |
| [`witness/node-id`](#field-witness-node-id) | `yes` | string |  |
| [`witness/role`](#field-witness-role) | `yes` | const: `admission-receipt` |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`witness/key`](#field-witness-key) | `yes` | string |  |
| [`valid/from`](#field-valid-from) | `yes` | string |  |
| [`valid/until`](#field-valid-until) | `yes` | string |  |
| [`delegation/sequence`](#field-delegation-sequence) | `yes` | integer |  |
| [`delegation/previous`](#field-delegation-previous) | `yes` | unspecified |  |
| [`signature`](#field-signature) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `witness-key-delegation.v1`

<a id="field-witness-node-id"></a>
## `witness/node-id`

- Required: `yes`
- Shape: string

<a id="field-witness-role"></a>
## `witness/role`

- Required: `yes`
- Shape: const: `admission-receipt`

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-witness-key"></a>
## `witness/key`

- Required: `yes`
- Shape: string

<a id="field-valid-from"></a>
## `valid/from`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid/until`

- Required: `yes`
- Shape: string

<a id="field-delegation-sequence"></a>
## `delegation/sequence`

- Required: `yes`
- Shape: integer

<a id="field-delegation-previous"></a>
## `delegation/previous`

- Required: `yes`
- Shape: unspecified

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object
