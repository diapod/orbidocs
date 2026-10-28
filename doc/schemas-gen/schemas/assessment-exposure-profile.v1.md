# Local Assessment Exposure Profile v1

Source schema: [`doc/schemas/assessment-exposure-profile.v1.schema.json`](../../schemas/assessment-exposure-profile.v1.schema.json)

P026 local pilot. Sealed-round is a reserved fail-closed boundary; no round execution is admitted. Empty protective-kind set preserves separate existing protection paths.

## Governing Basis

- [`doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`](../../project/40-proposals/026-resource-opinions-and-discussion-surfaces.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `assessment-exposure-profile.v1` |  |
| [`profile/id`](#field-profile-id) | `yes` | string |  |
| [`mode`](#field-mode) | `yes` | enum: `open`, `blind-until-own-judgment`, `sealed-round` |  |
| [`applies-to`](#field-applies-to) | `yes` | object |  |
| [`withheld`](#field-withheld) | `yes` | array |  |
| [`unlock`](#field-unlock) | `yes` | array |  |
| [`subject-window/seconds`](#field-subject-window-seconds) | `no` | integer |  |
| [`exempt/record-kinds`](#field-exempt-record-kinds) | `yes` | const: `[]` |  |
| [`guarantee`](#field-guarantee) | `yes` | const: `local-display-only` |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "unlock"
  ],
  "properties": {
    "unlock": {
      "contains": {
        "const": "subject-window-elapsed"
      }
    }
  }
}
```

Then:

```json
{
  "required": [
    "subject-window/seconds"
  ]
}
```

### Rule 2

When:

```json
{
  "required": [
    "mode"
  ],
  "properties": {
    "mode": {
      "const": "open"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "withheld": {
      "maxItems": 0
    },
    "unlock": {
      "maxItems": 0
    }
  },
  "not": {
    "required": [
      "subject-window/seconds"
    ]
  }
}
```

### Rule 3

When:

```json
{
  "required": [
    "mode"
  ],
  "properties": {
    "mode": {
      "const": "blind-until-own-judgment"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "unlock": {
      "minItems": 1
    },
    "withheld": {
      "allOf": [
        {
          "contains": {
            "const": "peer-ratings"
          }
        },
        {
          "contains": {
            "const": "peer-rationales"
          }
        },
        {
          "contains": {
            "const": "aggregates"
          }
        },
        {
          "contains": {
            "const": "counts"
          }
        },
        {
          "contains": {
            "const": "rating-order"
          }
        },
        {
          "contains": {
            "const": "popularity-badges"
          }
        }
      ]
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `assessment-exposure-profile.v1`

<a id="field-profile-id"></a>
## `profile/id`

- Required: `yes`
- Shape: string

<a id="field-mode"></a>
## `mode`

- Required: `yes`
- Shape: enum: `open`, `blind-until-own-judgment`, `sealed-round`

<a id="field-applies-to"></a>
## `applies-to`

- Required: `yes`
- Shape: object

<a id="field-withheld"></a>
## `withheld`

- Required: `yes`
- Shape: array

<a id="field-unlock"></a>
## `unlock`

- Required: `yes`
- Shape: array

<a id="field-subject-window-seconds"></a>
## `subject-window/seconds`

- Required: `no`
- Shape: integer

<a id="field-exempt-record-kinds"></a>
## `exempt/record-kinds`

- Required: `yes`
- Shape: const: `[]`

<a id="field-guarantee"></a>
## `guarantee`

- Required: `yes`
- Shape: const: `local-display-only`
