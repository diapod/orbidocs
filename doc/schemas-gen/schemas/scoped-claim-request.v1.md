# Scoped Claim Request v1

Source schema: [`doc/schemas/scoped-claim-request.v1.schema.json`](../../schemas/scoped-claim-request.v1.schema.json)

Verifier request for a bounded contextual nym claim proof.

## Governing Basis

- [`doc/project/40-proposals/081-horizontal-protocol-primitives.md`](../../project/40-proposals/081-horizontal-protocol-primitives.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `scoped-claim-request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`request/id`](#field-request-id) | `yes` | string |  |
| [`audience`](#field-audience) | `yes` | string |  |
| [`context/domain`](#field-context-domain) | `yes` | string |  |
| [`nonce`](#field-nonce) | `yes` | string |  |
| [`claims/requested`](#field-claims-requested) | `yes` | array |  |
| [`linkability/max`](#field-linkability-max) | `yes` | ref: `#/$defs/linkability` |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`claim`](#def-claim) | object |  |
| [`linkability`](#def-linkability) | enum: `one-shot`, `group-scoped`, `context-scoped` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `scoped-claim-request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-request-id"></a>
## `request/id`

- Required: `yes`
- Shape: string

<a id="field-audience"></a>
## `audience`

- Required: `yes`
- Shape: string

<a id="field-context-domain"></a>
## `context/domain`

- Required: `yes`
- Shape: string

<a id="field-nonce"></a>
## `nonce`

- Required: `yes`
- Shape: string

<a id="field-claims-requested"></a>
## `claims/requested`

- Required: `yes`
- Shape: array

<a id="field-linkability-max"></a>
## `linkability/max`

- Required: `yes`
- Shape: ref: `#/$defs/linkability`

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-claim"></a>
## `$defs.claim`

- Shape: object

<a id="def-linkability"></a>
## `$defs.linkability`

- Shape: enum: `one-shot`, `group-scoped`, `context-scoped`
