# Narrow Nym Succession v2

Source schema: [`doc/schemas/nym-succession.v2.schema.json`](../../schemas/nym-succession.v2.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-succession.v2` |  |
| [`succession/id`](#field-succession-id) | `yes` | string |  |
| [`succession/scope`](#field-succession-scope) | `yes` | enum: `line`, `case` |  |
| [`succession/purpose`](#field-succession-purpose) | `yes` | enum: `continue-line`, `continue-case` |  |
| [`predecessor/nym`](#field-predecessor-nym) | `yes` | string |  |
| [`predecessor/certificate`](#field-predecessor-certificate) | `no` | string |  |
| [`authorization/mode`](#field-authorization-mode) | `yes` | enum: `nym-key`, `continuity-key` |  |
| [`authorization/public-key`](#field-authorization-public-key) | `yes` | string |  |
| [`successor/nym`](#field-successor-nym) | `yes` | string |  |
| [`successor/certificate`](#field-successor-certificate) | `yes` | string |  |
| [`case/anchor`](#field-case-anchor) | `no` | string |  |
| [`audience`](#field-audience) | `no` | array | Named Ed25519 principals, including a private nym reader; this audience grant does not enable the nym kind as a case authority. |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`not-after`](#field-not-after) | `yes` | string |  |
| [`signatures`](#field-signatures) | `yes` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "succession/scope": {
      "const": "line"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "succession/purpose": {
      "const": "continue-line"
    },
    "authorization/mode": {
      "const": "nym-key"
    }
  },
  "required": [
    "predecessor/certificate"
  ],
  "not": {
    "anyOf": [
      {
        "required": [
          "case/anchor"
        ]
      },
      {
        "required": [
          "audience"
        ]
      }
    ]
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "succession/scope": {
      "const": "case"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "succession/purpose": {
      "const": "continue-case"
    },
    "authorization/mode": {
      "const": "continuity-key"
    }
  },
  "required": [
    "case/anchor",
    "audience"
  ],
  "not": {
    "required": [
      "predecessor/certificate"
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-succession.v2`

<a id="field-succession-id"></a>
## `succession/id`

- Required: `yes`
- Shape: string

<a id="field-succession-scope"></a>
## `succession/scope`

- Required: `yes`
- Shape: enum: `line`, `case`

<a id="field-succession-purpose"></a>
## `succession/purpose`

- Required: `yes`
- Shape: enum: `continue-line`, `continue-case`

<a id="field-predecessor-nym"></a>
## `predecessor/nym`

- Required: `yes`
- Shape: string

<a id="field-predecessor-certificate"></a>
## `predecessor/certificate`

- Required: `no`
- Shape: string

<a id="field-authorization-mode"></a>
## `authorization/mode`

- Required: `yes`
- Shape: enum: `nym-key`, `continuity-key`

<a id="field-authorization-public-key"></a>
## `authorization/public-key`

- Required: `yes`
- Shape: string

<a id="field-successor-nym"></a>
## `successor/nym`

- Required: `yes`
- Shape: string

<a id="field-successor-certificate"></a>
## `successor/certificate`

- Required: `yes`
- Shape: string

<a id="field-case-anchor"></a>
## `case/anchor`

- Required: `no`
- Shape: string

<a id="field-audience"></a>
## `audience`

- Required: `no`
- Shape: array

Named Ed25519 principals, including a private nym reader; this audience grant does not enable the nym kind as a case authority.

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

<a id="field-not-after"></a>
## `not-after`

- Required: `yes`
- Shape: string

<a id="field-signatures"></a>
## `signatures`

- Required: `yes`
- Shape: object
