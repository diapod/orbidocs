# Nym-authorship-readback.local.v1

Source schema: [`doc/schemas/nym-authorship-readback.local.v1.schema.json`](../../schemas/nym-authorship-readback.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-authorship-readback.local.v1` |  |
| [`operation/id`](#field-operation-id) | `yes` | string |  |
| [`certification/id`](#field-certification-id) | `yes` | string |  |
| [`state`](#field-state) | `yes` | enum: `review-required`, `preview-expired`, `signed` |  |
| [`preview/digest`](#field-preview-digest) | `yes` | string |  |
| [`document`](#field-document) | `yes` | object |  |
| [`record`](#field-record) | `yes` | unspecified |  |
| [`preview/expires-at`](#field-preview-expires-at) | `yes` | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "state": {
      "const": "signed"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "record": {
      "type": "object"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-authorship-readback.local.v1`

<a id="field-operation-id"></a>
## `operation/id`

- Required: `yes`
- Shape: string

<a id="field-certification-id"></a>
## `certification/id`

- Required: `yes`
- Shape: string

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `review-required`, `preview-expired`, `signed`

<a id="field-preview-digest"></a>
## `preview/digest`

- Required: `yes`
- Shape: string

<a id="field-document"></a>
## `document`

- Required: `yes`
- Shape: object

<a id="field-record"></a>
## `record`

- Required: `yes`
- Shape: unspecified

<a id="field-preview-expires-at"></a>
## `preview/expires-at`

- Required: `yes`
- Shape: string
