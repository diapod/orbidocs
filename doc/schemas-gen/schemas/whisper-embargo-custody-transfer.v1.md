# Whisper-embargo-custody-transfer.v1

Source schema: [`doc/schemas/whisper-embargo-custody-transfer.v1.schema.json`](../../schemas/whisper-embargo-custody-transfer.v1.schema.json)

Private plaintext for one authorized execution holder. Only carried inside an independently authorized end-sealed exchange. Verification does not establish actual custody or authorize publication.

## Governing Basis

- [`doc/project/40-proposals/013-whisper-social-signal-exchange/author-disclosure-conditions.md`](../../project/40-proposals/013-whisper-social-signal-exchange/author-disclosure-conditions.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-embargo-custody-transfer.v1` |  |
| [`recipient/node`](#field-recipient-node) | `yes` | string |  |
| [`registration/acceptance`](#field-registration-acceptance) | `yes` | string | Exact original authority-signed private acceptance, encoded as unpadded base64url. |
| [`proof/package`](#field-proof-package) | `yes` | ref: `whisper-release-proof-package.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-embargo-custody-transfer.v1`

<a id="field-recipient-node"></a>
## `recipient/node`

- Required: `yes`
- Shape: string

<a id="field-registration-acceptance"></a>
## `registration/acceptance`

- Required: `yes`
- Shape: string

Exact original authority-signed private acceptance, encoded as unpadded base64url.

<a id="field-proof-package"></a>
## `proof/package`

- Required: `yes`
- Shape: ref: `whisper-release-proof-package.v1.schema.json`
