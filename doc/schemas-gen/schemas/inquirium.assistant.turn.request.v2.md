# Assistant Preview and Execution Submission

Source schema: [`doc/schemas/inquirium.assistant.turn.request.v2.schema.json`](../../schemas/inquirium.assistant.turn.request.v2.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inquirium.assistant.turn.request.v2` |  |
| [`action`](#field-action) | `yes` | enum: `preview`, `execute` |  |
| [`request`](#field-request) | `yes` | object | The unchanged V1 operation request is validated by AssistantTurnRequest at the Schema Gate semantic boundary. |
| [`disclosure`](#field-disclosure) | `yes` | unspecified |  |
| [`acknowledgement`](#field-acknowledgement) | `yes` | unspecified |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "action"
  ],
  "properties": {
    "action": {
      "const": "preview"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "disclosure": {
      "type": "null"
    },
    "acknowledgement": {
      "type": "null"
    }
  }
}
```

### Rule 2

When:

```json
{
  "required": [
    "disclosure"
  ],
  "properties": {
    "disclosure": {
      "type": "object",
      "required": [
        "acknowledgement/required"
      ],
      "properties": {
        "acknowledgement/required": {
          "const": true
        }
      }
    }
  }
}
```

Then:

```json
{
  "properties": {
    "acknowledgement": {
      "type": "object"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.assistant.turn.request.v2`

<a id="field-action"></a>
## `action`

- Required: `yes`
- Shape: enum: `preview`, `execute`

<a id="field-request"></a>
## `request`

- Required: `yes`
- Shape: object

The unchanged V1 operation request is validated by AssistantTurnRequest at the Schema Gate semantic boundary.

<a id="field-disclosure"></a>
## `disclosure`

- Required: `yes`
- Shape: unspecified

<a id="field-acknowledgement"></a>
## `acknowledgement`

- Required: `yes`
- Shape: unspecified
