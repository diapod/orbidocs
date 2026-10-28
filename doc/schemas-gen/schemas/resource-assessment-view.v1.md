# Viewer-bound Resource Assessment View v1

Source schema: [`doc/schemas/resource-assessment-view.v1.schema.json`](../../schemas/resource-assessment-view.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`](../../project/40-proposals/026-resource-opinions-and-discussion-surfaces.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `resource-assessment-view.v1` |  |
| [`viewer/ref`](#field-viewer-ref) | `yes` | string |  |
| [`subject/key`](#field-subject-key) | `yes` | string |  |
| [`exposure`](#field-exposure) | `yes` | object |  |
| [`own`](#field-own) | `yes` | array |  |
| [`exempt`](#field-exempt) | `yes` | const: `[]` |  |
| [`peers`](#field-peers) | `yes` | unspecified |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "exposure"
  ],
  "properties": {
    "exposure": {
      "required": [
        "state"
      ],
      "properties": {
        "state": {
          "const": "released"
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
    "peers": {
      "type": "array"
    },
    "exposure": {
      "required": [
        "degraded"
      ],
      "properties": {
        "withheld": {
          "maxItems": 0
        },
        "unlock/options": {
          "maxItems": 0
        },
        "window": false
      }
    }
  }
}
```

### Rule 2

When:

```json
{
  "required": [
    "exposure"
  ],
  "properties": {
    "exposure": {
      "required": [
        "state"
      ],
      "properties": {
        "state": {
          "enum": [
            "withheld",
            "disclosure-not-recorded"
          ]
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
    "peers": {
      "type": "null"
    },
    "exposure": {
      "properties": {
        "degraded": false
      }
    }
  }
}
```

### Rule 3

When:

```json
{
  "required": [
    "exposure"
  ],
  "properties": {
    "exposure": {
      "required": [
        "state"
      ],
      "properties": {
        "state": {
          "const": "disclosure-not-recorded"
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
    "exposure": {
      "properties": {
        "withheld": {
          "maxItems": 0
        },
        "unlock/options": {
          "maxItems": 0
        },
        "window": false
      }
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `resource-assessment-view.v1`

<a id="field-viewer-ref"></a>
## `viewer/ref`

- Required: `yes`
- Shape: string

<a id="field-subject-key"></a>
## `subject/key`

- Required: `yes`
- Shape: string

<a id="field-exposure"></a>
## `exposure`

- Required: `yes`
- Shape: object

<a id="field-own"></a>
## `own`

- Required: `yes`
- Shape: array

<a id="field-exempt"></a>
## `exempt`

- Required: `yes`
- Shape: const: `[]`

<a id="field-peers"></a>
## `peers`

- Required: `yes`
- Shape: unspecified
