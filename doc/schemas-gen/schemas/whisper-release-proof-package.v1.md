# Whisper-release-proof-package.v1

Source schema: [`doc/schemas/whisper-release-proof-package.v1.schema.json`](../../schemas/whisper-release-proof-package.v1.schema.json)

Exact single-audience proof and approved payload opening, frozen before the authority commit.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-release-proof-package.v1` |  |
| [`audience/manifest`](#field-audience-manifest) | `yes` | ref: `whisper-embargo-audience-manifest.v1.schema.json` |  |
| [`anchor/manifest`](#field-anchor-manifest) | `yes` | ref: `whisper-embargo-manifest.v1.schema.json` |  |
| [`anchor/profile`](#field-anchor-profile) | `yes` | unspecified |  |
| [`anchor/receipt`](#field-anchor-receipt) | `yes` | unspecified |  |
| [`payload/bytes`](#field-payload-bytes) | `yes` | string |  |
| [`payload/nonce`](#field-payload-nonce) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-release-proof-package.v1`

<a id="field-audience-manifest"></a>
## `audience/manifest`

- Required: `yes`
- Shape: ref: `whisper-embargo-audience-manifest.v1.schema.json`

<a id="field-anchor-manifest"></a>
## `anchor/manifest`

- Required: `yes`
- Shape: ref: `whisper-embargo-manifest.v1.schema.json`

<a id="field-anchor-profile"></a>
## `anchor/profile`

- Required: `yes`
- Shape: unspecified

<a id="field-anchor-receipt"></a>
## `anchor/receipt`

- Required: `yes`
- Shape: unspecified

<a id="field-payload-bytes"></a>
## `payload/bytes`

- Required: `yes`
- Shape: string

<a id="field-payload-nonce"></a>
## `payload/nonce`

- Required: `yes`
- Shape: string
