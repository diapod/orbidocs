# INAC Historical Admission Result

Source schema: [`doc/schemas/inac-admission-status.result.v1.schema.json`](../../schemas/inac-admission-status.result.v1.schema.json)

## Governing Basis

- [`doc/project/60-solutions/027-messaging-middleware/027-messaging-middleware.md#consent-loss-recovery`](../../project/60-solutions/027-messaging-middleware/027-messaging-middleware.md#consent-loss-recovery)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inac-admission-status.result.v1` |  |
| [`outcome`](#field-outcome) | `yes` | enum: `accepted`, `already-present`, `rejected`, `unknown`, `unavailable` |  |
| [`observed/at`](#field-observed-at) | `yes` | string |  |
| [`admission/id`](#field-admission-id) | `no` | string |  |
| [`support`](#field-support) | `no` | ref: `messaging-admission-identity.v1.schema.json` |  |
| [`refusal`](#field-refusal) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "outcome": {
      "enum": [
        "accepted",
        "already-present"
      ]
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
    "admission/id"
  ],
  "not": {
    "required": [
      "refusal"
    ]
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "outcome": {
      "enum": [
        "unknown",
        "unavailable"
      ]
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
  "not": {
    "anyOf": [
      {
        "required": [
          "admission/id"
        ]
      },
      {
        "required": [
          "refusal"
        ]
      }
    ]
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "outcome": {
      "const": "rejected"
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
    "refusal"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inac-admission-status.result.v1`

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: enum: `accepted`, `already-present`, `rejected`, `unknown`, `unavailable`

<a id="field-observed-at"></a>
## `observed/at`

- Required: `yes`
- Shape: string

<a id="field-admission-id"></a>
## `admission/id`

- Required: `no`
- Shape: string

<a id="field-support"></a>
## `support`

- Required: `no`
- Shape: ref: `messaging-admission-identity.v1.schema.json`

<a id="field-refusal"></a>
## `refusal`

- Required: `no`
- Shape: object
