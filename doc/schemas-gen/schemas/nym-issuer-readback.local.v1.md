# Nym-issuer-readback.local.v1

Source schema: [`doc/schemas/nym-issuer-readback.local.v1.schema.json`](../../schemas/nym-issuer-readback.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-issuer-readback.local.v1` |  |
| [`exchange/digest`](#field-exchange-digest) | `yes` | string |  |
| [`state`](#field-state) | `yes` | enum: `decision-prepared`, `not-found-or-expired` |  |
| [`artifact/digest`](#field-artifact-digest) | `yes` | unspecified |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "state": {
      "const": "not-found-or-expired"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "artifact/digest": {
      "type": "null"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-issuer-readback.local.v1`

<a id="field-exchange-digest"></a>
## `exchange/digest`

- Required: `yes`
- Shape: string

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `decision-prepared`, `not-found-or-expired`

<a id="field-artifact-digest"></a>
## `artifact/digest`

- Required: `yes`
- Shape: unspecified
