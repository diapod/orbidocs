# Scoped Claim Presentation v1

Source schema: [`doc/schemas/scoped-claim-presentation.v1.schema.json`](../../schemas/scoped-claim-presentation.v1.schema.json)

Suite-neutral bounded nym claim presentation. Verification yields evidence values, not authorization.

## Governing Basis

- [`doc/project/40-proposals/081-horizontal-protocol-primitives.md`](../../project/40-proposals/081-horizontal-protocol-primitives.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `scoped-claim-presentation.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`presentation/id`](#field-presentation-id) | `yes` | string |  |
| [`request/ref`](#field-request-ref) | `yes` | string |  |
| [`request/digest`](#field-request-digest) | `yes` | ref: `#/$defs/sha256_digest` |  |
| [`subject/kind`](#field-subject-kind) | `yes` | const: `nym` |  |
| [`subject/id`](#field-subject-id) | `yes` | string |  |
| [`audience`](#field-audience) | `yes` | string |  |
| [`context/domain`](#field-context-domain) | `yes` | string |  |
| [`nonce`](#field-nonce) | `yes` | string |  |
| [`claims/proven`](#field-claims-proven) | `yes` | array |  |
| [`proof/suite`](#field-proof-suite) | `yes` | enum: `orbiplex.nym-ed25519-cert.v1` |  |
| [`proof/material`](#field-proof-material) | `yes` | object |  |
| [`linkability/scope`](#field-linkability-scope) | `yes` | ref: `#/$defs/linkability` |  |
| [`nullifier`](#field-nullifier) | `no` | string \| null |  |
| [`revocation/evidence-ref`](#field-revocation-evidence-ref) | `no` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`claim`](#def-claim) | object |  |
| [`linkability`](#def-linkability) | enum: `one-shot`, `group-scoped`, `context-scoped` |  |
| [`sha256_digest`](#def-sha256-digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `scoped-claim-presentation.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-presentation-id"></a>
## `presentation/id`

- Required: `yes`
- Shape: string

<a id="field-request-ref"></a>
## `request/ref`

- Required: `yes`
- Shape: string

<a id="field-request-digest"></a>
## `request/digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256_digest`

<a id="field-subject-kind"></a>
## `subject/kind`

- Required: `yes`
- Shape: const: `nym`

<a id="field-subject-id"></a>
## `subject/id`

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

<a id="field-claims-proven"></a>
## `claims/proven`

- Required: `yes`
- Shape: array

<a id="field-proof-suite"></a>
## `proof/suite`

- Required: `yes`
- Shape: enum: `orbiplex.nym-ed25519-cert.v1`

<a id="field-proof-material"></a>
## `proof/material`

- Required: `yes`
- Shape: object

<a id="field-linkability-scope"></a>
## `linkability/scope`

- Required: `yes`
- Shape: ref: `#/$defs/linkability`

<a id="field-nullifier"></a>
## `nullifier`

- Required: `no`
- Shape: string | null

<a id="field-revocation-evidence-ref"></a>
## `revocation/evidence-ref`

- Required: `no`
- Shape: string

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

<a id="def-sha256-digest"></a>
## `$defs.sha256_digest`

- Shape: string
