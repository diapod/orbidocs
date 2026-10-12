# Opaque Matrix Agora Carrier v1

Source schema: [`doc/schemas/agora-matrix-carrier.v1.schema.json`](../../schemas/agora-matrix-carrier.v1.schema.json)

P035-004 event content for org.orbiplex.agora.record.v2. The decoded bytes are the immutable signed author envelope, excluding local relay observations. Strict parsing additionally rejects duplicate decoded object keys and noncanonical base64url trailing bits.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agora-matrix-carrier.v1` |  |
| [`envelope/encoding`](#field-envelope-encoding) | `yes` | const: `base64url` |  |
| [`envelope/bytes`](#field-envelope-bytes) | `yes` | string |  |
| [`relay/id`](#field-relay-id) | `yes` | string |  |
| [`relay/hops`](#field-relay-hops) | `yes` | integer |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agora-matrix-carrier.v1`

<a id="field-envelope-encoding"></a>
## `envelope/encoding`

- Required: `yes`
- Shape: const: `base64url`

<a id="field-envelope-bytes"></a>
## `envelope/bytes`

- Required: `yes`
- Shape: string

<a id="field-relay-id"></a>
## `relay/id`

- Required: `yes`
- Shape: string

<a id="field-relay-hops"></a>
## `relay/hops`

- Required: `yes`
- Shape: integer
