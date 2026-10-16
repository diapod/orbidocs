# Issuance-revocation-status.v1

Source schema: [`doc/schemas/issuance-revocation-status.v1.schema.json`](../../schemas/issuance-revocation-status.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/076-limited-messaging-grants-decision.md`](../../project/40-proposals/076-limited-messaging-grants-decision.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `issuance-revocation-status.v1` |  |
| [`federation_id`](#field-federation-id) | `yes` | string |  |
| [`delegation_id`](#field-delegation-id) | `yes` | string |  |
| [`delegation_digest`](#field-delegation-digest) | `yes` | string |  |
| [`revision`](#field-revision) | `yes` | integer |  |
| [`as_of`](#field-as-of) | `yes` | string |  |
| [`valid_until`](#field-valid-until) | `yes` | string |  |
| [`status`](#field-status) | `yes` | enum: `active`, `revoked` |  |
| [`revoked_passport_ids`](#field-revoked-passport-ids) | `yes` | array |  |
| [`signature`](#field-signature) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `issuance-revocation-status.v1`

<a id="field-federation-id"></a>
## `federation_id`

- Required: `yes`
- Shape: string

<a id="field-delegation-id"></a>
## `delegation_id`

- Required: `yes`
- Shape: string

<a id="field-delegation-digest"></a>
## `delegation_digest`

- Required: `yes`
- Shape: string

<a id="field-revision"></a>
## `revision`

- Required: `yes`
- Shape: integer

<a id="field-as-of"></a>
## `as_of`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid_until`

- Required: `yes`
- Shape: string

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `active`, `revoked`

<a id="field-revoked-passport-ids"></a>
## `revoked_passport_ids`

- Required: `yes`
- Shape: array

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object
