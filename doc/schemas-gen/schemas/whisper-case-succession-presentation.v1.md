# Whisper-case-succession-presentation.v1

Source schema: [`doc/schemas/whisper-case-succession-presentation.v1.schema.json`](../../schemas/whisper-case-succession-presentation.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-case-succession-presentation.v1` |  |
| [`profile`](#field-profile) | `yes` | enum: `carried`, `referenced` |  |
| [`case/anchor`](#field-case-anchor) | `yes` | string |  |
| [`evidence`](#field-evidence) | `yes` | array |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "profile": {
      "const": "carried"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "evidence": {
      "items": {
        "required": [
          "bytes"
        ]
      }
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-case-succession-presentation.v1`

<a id="field-profile"></a>
## `profile`

- Required: `yes`
- Shape: enum: `carried`, `referenced`

<a id="field-case-anchor"></a>
## `case/anchor`

- Required: `yes`
- Shape: string

<a id="field-evidence"></a>
## `evidence`

- Required: `yes`
- Shape: array
