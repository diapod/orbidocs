# Agora-admission-request.v1

Source schema: [`doc/schemas/agora-admission-request.v1.schema.json`](../../schemas/agora-admission-request.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agora-admission-request.v1` |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`status/digest`](#field-status-digest) | `yes` | string |  |
| [`receipt/profile`](#field-receipt-profile) | `yes` | enum: `full-record`, `detached-manifest` |  |
| [`material`](#field-material) | `yes` | ref: `agora-admission-material.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agora-admission-request.v1`

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-status-digest"></a>
## `status/digest`

- Required: `yes`
- Shape: string

<a id="field-receipt-profile"></a>
## `receipt/profile`

- Required: `yes`
- Shape: enum: `full-record`, `detached-manifest`

<a id="field-material"></a>
## `material`

- Required: `yes`
- Shape: ref: `agora-admission-material.v1.schema.json`
