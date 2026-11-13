# Agora-source-attestation-request.local.v1

Source schema: [`doc/schemas/agora-source-attestation-request.local.v1.schema.json`](../../schemas/agora-source-attestation-request.local.v1.schema.json)

Exact immutable profile and independently adopted source-policy bytes. The record is identified only by the route; historical facts and times come exclusively from its owner.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agora-source-attestation-request.local.v1` |  |
| [`profile/bytes`](#field-profile-bytes) | `yes` | string |  |
| [`policy/bytes`](#field-policy-bytes) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agora-source-attestation-request.local.v1`

<a id="field-profile-bytes"></a>
## `profile/bytes`

- Required: `yes`
- Shape: string

<a id="field-policy-bytes"></a>
## `policy/bytes`

- Required: `yes`
- Shape: string
