# Agora Vault Ref v1

Source schema: [`doc/schemas/agora-vault-ref.v1.schema.json`](../../schemas/agora-vault-ref.v1.schema.json)

Plaintext record shape intended to be sealed inside pseudonym-vault.v1. It maps recovered participant or nym material to an opaque Agora Vault subject and capability references.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agora-vault-ref.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`ref/id`](#field-ref-id) | `yes` | string |  |
| [`agora/provider-ref`](#field-agora-provider-ref) | `yes` | string |  |
| [`vault/subject`](#field-vault-subject) | `yes` | string | Opaque storage partition. It must not encode participant or nym ids. |
| [`allowed/artifact-kinds`](#field-allowed-artifact-kinds) | `yes` | array |  |
| [`capability/refs`](#field-capability-refs) | `yes` | array |  |
| [`created/at`](#field-created-at) | `yes` | string |  |
| [`last/seen-at`](#field-last-seen-at) | `no` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agora-vault-ref.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-ref-id"></a>
## `ref/id`

- Required: `yes`
- Shape: string

<a id="field-agora-provider-ref"></a>
## `agora/provider-ref`

- Required: `yes`
- Shape: string

<a id="field-vault-subject"></a>
## `vault/subject`

- Required: `yes`
- Shape: string

Opaque storage partition. It must not encode participant or nym ids.

<a id="field-allowed-artifact-kinds"></a>
## `allowed/artifact-kinds`

- Required: `yes`
- Shape: array

<a id="field-capability-refs"></a>
## `capability/refs`

- Required: `yes`
- Shape: array

<a id="field-created-at"></a>
## `created/at`

- Required: `yes`
- Shape: string

<a id="field-last-seen-at"></a>
## `last/seen-at`

- Required: `no`
- Shape: string
