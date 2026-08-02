# Implementation Limit Classification v1

Source schema: [`doc/schemas/limit-classification.v1.schema.json`](../../schemas/limit-classification.v1.schema.json)

Reviewed classification and evidence record for one compiled implementation limit.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `limit-classification.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`classification/ref`](#field-classification-ref) | `yes` | string |  |
| [`limit/id`](#field-limit-id) | `yes` | string |  |
| [`implementation/symbol`](#field-implementation-symbol) | `yes` | string |  |
| [`implementation/source`](#field-implementation-source) | `yes` | string |  |
| [`current/value`](#field-current-value) | `yes` | integer |  |
| [`current/unit`](#field-current-unit) | `yes` | string |  |
| [`class`](#field-class) | `yes` | enum: `normative`, `boundary-safety`, `federated`, `operational`, `unclassified` |  |
| [`owner`](#field-owner) | `yes` | string |  |
| [`merge/direction`](#field-merge-direction) | `yes` | enum: `none`, `min`, `max`, `intersect`, `domain` |  |
| [`operator/override`](#field-operator-override) | `yes` | enum: `forbidden`, `tighten-only`, `bounded` |  |
| [`evidence`](#field-evidence) | `yes` | object |  |
| [`review`](#field-review) | `yes` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "class": {
      "const": "normative"
    }
  },
  "required": [
    "class"
  ]
}
```

Then:

```json
{
  "properties": {
    "merge/direction": {
      "const": "none"
    },
    "operator/override": {
      "const": "forbidden"
    },
    "evidence": {
      "properties": {
        "status": {
          "const": "not-required"
        },
        "test/refs": {
          "maxItems": 0
        }
      },
      "not": {
        "anyOf": [
          {
            "required": [
              "threatened/resource"
            ]
          },
          {
            "required": [
              "refusal/layer"
            ]
          }
        ]
      }
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "class": {
      "const": "boundary-safety"
    }
  },
  "required": [
    "class"
  ]
}
```

Then:

```json
{
  "properties": {
    "merge/direction": {
      "enum": [
        "min",
        "max",
        "intersect",
        "domain"
      ]
    },
    "operator/override": {
      "const": "tighten-only"
    },
    "evidence": {
      "required": [
        "threatened/resource",
        "refusal/layer"
      ],
      "properties": {
        "status": {
          "const": "proven"
        },
        "refusal/layer": {
          "const": "pre-policy"
        },
        "test/refs": {
          "minItems": 1
        }
      }
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "class": {
      "enum": [
        "federated",
        "operational"
      ]
    }
  },
  "required": [
    "class"
  ]
}
```

Then:

```json
{
  "properties": {
    "merge/direction": {
      "enum": [
        "min",
        "max",
        "intersect",
        "domain"
      ]
    },
    "operator/override": {
      "enum": [
        "tighten-only",
        "bounded"
      ]
    },
    "evidence": {
      "properties": {
        "status": {
          "const": "not-required"
        },
        "test/refs": {
          "maxItems": 0
        }
      },
      "not": {
        "anyOf": [
          {
            "required": [
              "threatened/resource"
            ]
          },
          {
            "required": [
              "refusal/layer"
            ]
          }
        ]
      }
    }
  }
}
```

### Rule 4

When:

```json
{
  "properties": {
    "class": {
      "const": "unclassified"
    }
  },
  "required": [
    "class"
  ]
}
```

Then:

```json
{
  "properties": {
    "merge/direction": {
      "const": "none"
    },
    "operator/override": {
      "const": "forbidden"
    },
    "evidence": {
      "required": [
        "threatened/resource"
      ],
      "properties": {
        "status": {
          "const": "pending"
        },
        "test/refs": {
          "maxItems": 0
        }
      },
      "not": {
        "required": [
          "refusal/layer"
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
- Shape: const: `limit-classification.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-classification-ref"></a>
## `classification/ref`

- Required: `yes`
- Shape: string

<a id="field-limit-id"></a>
## `limit/id`

- Required: `yes`
- Shape: string

<a id="field-implementation-symbol"></a>
## `implementation/symbol`

- Required: `yes`
- Shape: string

<a id="field-implementation-source"></a>
## `implementation/source`

- Required: `yes`
- Shape: string

<a id="field-current-value"></a>
## `current/value`

- Required: `yes`
- Shape: integer

<a id="field-current-unit"></a>
## `current/unit`

- Required: `yes`
- Shape: string

<a id="field-class"></a>
## `class`

- Required: `yes`
- Shape: enum: `normative`, `boundary-safety`, `federated`, `operational`, `unclassified`

<a id="field-owner"></a>
## `owner`

- Required: `yes`
- Shape: string

<a id="field-merge-direction"></a>
## `merge/direction`

- Required: `yes`
- Shape: enum: `none`, `min`, `max`, `intersect`, `domain`

<a id="field-operator-override"></a>
## `operator/override`

- Required: `yes`
- Shape: enum: `forbidden`, `tighten-only`, `bounded`

<a id="field-evidence"></a>
## `evidence`

- Required: `yes`
- Shape: object

<a id="field-review"></a>
## `review`

- Required: `yes`
- Shape: object
