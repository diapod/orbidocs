# Bounded HTTP Fetch Artifact Read Result v1

Source schema: [`doc/schemas/bounded-http-fetch-artifact-read-result.v1.schema.json`](../../schemas/bounded-http-fetch-artifact-read-result.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `bounded-http-fetch-artifact-read-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`outcome`](#field-outcome) | `yes` | enum: `completed`, `refused`, `failed` |  |
| [`artifact/ref`](#field-artifact-ref) | `yes` | string |  |
| [`artifact/digest`](#field-artifact-digest) | `yes` | ref: `#/$defs/sha256Digest` |  |
| [`artifact/size-bytes`](#field-artifact-size-bytes) | `yes` | integer |  |
| [`body/base64`](#field-body-base64) | `no` | string |  |
| [`failure/code`](#field-failure-code) | `no` | enum: `consumer-denied`, `artifact-unavailable`, `artifact-binding-mismatch`, `artifact-size-limit`, `artifact-transfer-expired` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`sha256Digest`](#def-sha256digest) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "outcome": {
      "const": "completed"
    }
  },
  "required": [
    "outcome"
  ]
}
```

Then:

```json
{
  "required": [
    "body/base64"
  ],
  "not": {
    "required": [
      "failure/code"
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `bounded-http-fetch-artifact-read-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: enum: `completed`, `refused`, `failed`

<a id="field-artifact-ref"></a>
## `artifact/ref`

- Required: `yes`
- Shape: string

<a id="field-artifact-digest"></a>
## `artifact/digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256Digest`

<a id="field-artifact-size-bytes"></a>
## `artifact/size-bytes`

- Required: `yes`
- Shape: integer

<a id="field-body-base64"></a>
## `body/base64`

- Required: `no`
- Shape: string

<a id="field-failure-code"></a>
## `failure/code`

- Required: `no`
- Shape: enum: `consumer-denied`, `artifact-unavailable`, `artifact-binding-mismatch`, `artifact-size-limit`, `artifact-transfer-expired`

## Definition Semantics

<a id="def-sha256digest"></a>
## `$defs.sha256Digest`

- Shape: string
