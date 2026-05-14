# Service CA Revocation v1

Source schema: [`doc/schemas/service-ca-revocation.v1.schema.json`](../../schemas/service-ca-revocation.v1.schema.json)

Signed governance or operator fact revoking scoped Service CA material. This is a revocation candidate until the local node verifies the signature and accepts the issuer under local trust policy.

## Governing Basis

- [`doc/project/40-proposals/056-orbiplex-tls-trust-policy.md`](../../project/40-proposals/056-orbiplex-tls-trust-policy.md)
- [`doc/project/60-solutions/024-tls-trust-policy/024-tls-trust-policy.md`](../../project/60-solutions/024-tls-trust-policy/024-tls-trust-policy.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `service-ca-revocation.v1` |  |
| [`revocation/id`](#field-revocation-id) | `yes` | string |  |
| [`ca/id`](#field-ca-id) | `yes` | string |  |
| [`material/digest`](#field-material-digest) | `no` | ref: `#/$defs/sha256Digest` | Optional canonical payload or PEM digest. When omitted, the revocation applies to all active local candidates with the same `ca/id`. |
| [`revoked/at`](#field-revoked-at) | `yes` | string |  |
| [`reason-code`](#field-reason-code) | `yes` | enum: `key-compromise`, `scope-withdrawn`, `superseded`, `operator-request`, `policy-violation`, `diagnostic` |  |
| [`issuer`](#field-issuer) | `yes` | ref: `#/$defs/issuer` |  |
| [`policy/ref`](#field-policy-ref) | `no` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`issuer`](#def-issuer) | object |  |
| [`signature`](#def-signature) | object |  |
| [`sha256Digest`](#def-sha256digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `service-ca-revocation.v1`

<a id="field-revocation-id"></a>
## `revocation/id`

- Required: `yes`
- Shape: string

<a id="field-ca-id"></a>
## `ca/id`

- Required: `yes`
- Shape: string

<a id="field-material-digest"></a>
## `material/digest`

- Required: `no`
- Shape: ref: `#/$defs/sha256Digest`

Optional canonical payload or PEM digest. When omitted, the revocation applies to all active local candidates with the same `ca/id`.

<a id="field-revoked-at"></a>
## `revoked/at`

- Required: `yes`
- Shape: string

<a id="field-reason-code"></a>
## `reason-code`

- Required: `yes`
- Shape: enum: `key-compromise`, `scope-withdrawn`, `superseded`, `operator-request`, `policy-violation`, `diagnostic`

<a id="field-issuer"></a>
## `issuer`

- Required: `yes`
- Shape: ref: `#/$defs/issuer`

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `no`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

## Definition Semantics

<a id="def-issuer"></a>
## `$defs.issuer`

- Shape: object

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object

<a id="def-sha256digest"></a>
## `$defs.sha256Digest`

- Shape: string
