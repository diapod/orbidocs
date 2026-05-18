# Seed Directory Query Attestation v1

Source schema: [`doc/schemas/seed-directory-query-attestation.v1.schema.json`](../../schemas/seed-directory-query-attestation.v1.schema.json)

Signed proof for one Seed Directory query response. It binds the normalized query path/filter to the canonical response digest and the local projection high-water mark. This attests what the directory returned; it does not by itself prove that the returned world-state is globally true.

## Governing Basis

- [`doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`](../../project/40-proposals/054-user-maintained-federated-seed-directory.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `seed-directory-query-attestation.v1` | Schema discriminator. MUST be exactly `seed-directory-query-attestation.v1`. |
| [`attestation/id`](#field-attestation-id) | `yes` | string | Stable identifier for this attested response. The reference implementation derives it from `result/digest`. |
| [`directory/node-id`](#field-directory-node-id) | `yes` | string | Node id of the Seed Directory instance that assembled the response. |
| [`query/mode`](#field-query-mode) | `yes` | enum: `adv-get`, `adv-list`, `cap-node`, `cap-query`, `revocations` | Read surface being attested. |
| [`query/path`](#field-query-path) | `yes` | string | HTTP path without query string. |
| [`query/filter`](#field-query-filter) | `yes` | object | URL-decoded query parameters after removing the `attest` trigger. |
| [`result/digest`](#field-result-digest) | `yes` | string | Digest of the canonical JSON response body before the attestation is attached. |
| [`result/digest-alg`](#field-result-digest-alg) | `yes` | const: `jcs-nfc-sha256-base64url` | Canonicalization and digest algorithm used for `result/digest`. |
| [`projection/high-water-tx-id`](#field-projection-high-water-tx-id) | `yes` | integer \| null | Highest temporal projection transaction id visible when the response was assembled, or null if the projection has no temporal facts yet. |
| [`policy/id`](#field-policy-id) | `no` | string | Optional local policy id that governed this query. |
| [`policy/digest`](#field-policy-digest) | `no` | string | Optional digest of the local policy material. |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`signer/id`](#field-signer-id) | `yes` | string | Signer id used for the attestation signature. |
| [`signature`](#field-signature) | `yes` | object | Signature over canonical JSON of this object with `signature` omitted. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `seed-directory-query-attestation.v1`

Schema discriminator. MUST be exactly `seed-directory-query-attestation.v1`.

<a id="field-attestation-id"></a>
## `attestation/id`

- Required: `yes`
- Shape: string

Stable identifier for this attested response. The reference implementation derives it from `result/digest`.

<a id="field-directory-node-id"></a>
## `directory/node-id`

- Required: `yes`
- Shape: string

Node id of the Seed Directory instance that assembled the response.

<a id="field-query-mode"></a>
## `query/mode`

- Required: `yes`
- Shape: enum: `adv-get`, `adv-list`, `cap-node`, `cap-query`, `revocations`

Read surface being attested.

<a id="field-query-path"></a>
## `query/path`

- Required: `yes`
- Shape: string

HTTP path without query string.

<a id="field-query-filter"></a>
## `query/filter`

- Required: `yes`
- Shape: object

URL-decoded query parameters after removing the `attest` trigger.

<a id="field-result-digest"></a>
## `result/digest`

- Required: `yes`
- Shape: string

Digest of the canonical JSON response body before the attestation is attached.

<a id="field-result-digest-alg"></a>
## `result/digest-alg`

- Required: `yes`
- Shape: const: `jcs-nfc-sha256-base64url`

Canonicalization and digest algorithm used for `result/digest`.

<a id="field-projection-high-water-tx-id"></a>
## `projection/high-water-tx-id`

- Required: `yes`
- Shape: integer | null

Highest temporal projection transaction id visible when the response was assembled, or null if the projection has no temporal facts yet.

<a id="field-policy-id"></a>
## `policy/id`

- Required: `no`
- Shape: string

Optional local policy id that governed this query.

<a id="field-policy-digest"></a>
## `policy/digest`

- Required: `no`
- Shape: string

Optional digest of the local policy material.

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-signer-id"></a>
## `signer/id`

- Required: `yes`
- Shape: string

Signer id used for the attestation signature.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object

Signature over canonical JSON of this object with `signature` omitted.
