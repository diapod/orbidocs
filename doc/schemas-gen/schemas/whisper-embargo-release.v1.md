# Whisper-embargo-release.v1

Source schema: [`doc/schemas/whisper-embargo-release.v1.schema.json`](../../schemas/whisper-embargo-release.v1.schema.json)

Content of the executor-signed Agora release envelope. The statement carries its exact canonical bytes.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-embargo-release.v1` |  |
| [`intent`](#field-intent) | `yes` | ref: `whisper-release-intent.v1.schema.json` |  |
| [`proof/package`](#field-proof-package) | `yes` | ref: `whisper-release-proof-package.v1.schema.json` |  |
| [`commit/statement`](#field-commit-statement) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-embargo-release.v1`

<a id="field-intent"></a>
## `intent`

- Required: `yes`
- Shape: ref: `whisper-release-intent.v1.schema.json`

<a id="field-proof-package"></a>
## `proof/package`

- Required: `yes`
- Shape: ref: `whisper-release-proof-package.v1.schema.json`

<a id="field-commit-statement"></a>
## `commit/statement`

- Required: `yes`
- Shape: string
