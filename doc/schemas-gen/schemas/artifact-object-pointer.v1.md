# Artifact Object Pointer v1

Source schema: [`doc/schemas/artifact-object-pointer.v1.schema.json`](../../schemas/artifact-object-pointer.v1.schema.json)

Small Artifact Delivery control artifact pointing to a host-owned object-store payload. The pointer is not authority: receivers MUST fetch the object, verify digest, size, expiry, and local transport policy, then admit the original artifact through normal Artifact Delivery admission.

## Governing Basis

- [`doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`](../../project/60-solutions/023-artifact-delivery/023-artifact-delivery.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `artifact-object-pointer.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`pointer/id`](#field-pointer-id) | `yes` | string |  |
| [`artifact/schema`](#field-artifact-schema) | `yes` | string |  |
| [`artifact/content-type`](#field-artifact-content-type) | `yes` | string |  |
| [`artifact/digest`](#field-artifact-digest) | `yes` | string |  |
| [`artifact/size-bytes`](#field-artifact-size-bytes) | `yes` | integer |  |
| [`store/scheme`](#field-store-scheme) | `yes` | enum: `daemon-object-store` |  |
| [`store/ref`](#field-store-ref) | `yes` | string |  |
| [`fetch/url`](#field-fetch-url) | `no` | string | Receiver-side HTTPS or loopback fetch URL for the bounded object fetch endpoint. The URL is transport metadata; receivers MUST still verify digest, size, expiry, and local policy before admission. |
| [`fetch/token-ref`](#field-fetch-token-ref) | `no` | string | Optional bounded fetch-token reference. The token value itself MUST NOT be embedded when the pointer is visible to logs or untrusted intermediaries. |
| [`payload/security`](#field-payload-security) | `no` | enum: `sealed`, `integrity-only` |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `artifact-object-pointer.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-pointer-id"></a>
## `pointer/id`

- Required: `yes`
- Shape: string

<a id="field-artifact-schema"></a>
## `artifact/schema`

- Required: `yes`
- Shape: string

<a id="field-artifact-content-type"></a>
## `artifact/content-type`

- Required: `yes`
- Shape: string

<a id="field-artifact-digest"></a>
## `artifact/digest`

- Required: `yes`
- Shape: string

<a id="field-artifact-size-bytes"></a>
## `artifact/size-bytes`

- Required: `yes`
- Shape: integer

<a id="field-store-scheme"></a>
## `store/scheme`

- Required: `yes`
- Shape: enum: `daemon-object-store`

<a id="field-store-ref"></a>
## `store/ref`

- Required: `yes`
- Shape: string

<a id="field-fetch-url"></a>
## `fetch/url`

- Required: `no`
- Shape: string

Receiver-side HTTPS or loopback fetch URL for the bounded object fetch endpoint. The URL is transport metadata; receivers MUST still verify digest, size, expiry, and local policy before admission.

<a id="field-fetch-token-ref"></a>
## `fetch/token-ref`

- Required: `no`
- Shape: string

Optional bounded fetch-token reference. The token value itself MUST NOT be embedded when the pointer is visible to logs or untrusted intermediaries.

<a id="field-payload-security"></a>
## `payload/security`

- Required: `no`
- Shape: enum: `sealed`, `integrity-only`

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string
