# NSE Hook Offer v1

Source schema: [`doc/schemas/nse-hook-offer.v1.schema.json`](../../schemas/nse-hook-offer.v1.schema.json)

Exact host-built offer for one NSE invocation. V1 admits model selection and the closed reference-set policy-hook family.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nse-hook-offer.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`invocation/ref`](#field-invocation-ref) | `yes` | string |  |
| [`hook/id`](#field-hook-id) | `yes` | ref: `#/$defs/hook-id` |  |
| [`hook/v`](#field-hook-v) | `yes` | const: `1` |  |
| [`hook/class`](#field-hook-class) | `yes` | enum: `select`, `order`, `narrow`, `restrict`, `raise-risk`, `select-profile` |  |
| [`offer/digest`](#field-offer-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`causal/ref`](#field-causal-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`backend/bounds`](#field-backend-bounds) | `yes` | object |  |
| [`payload`](#field-payload) | `yes` | unspecified |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`hook-id`](#def-hook-id) | enum: `select-llm-model`, `assemble-prompt`, `select-output-schema`, `select-repair-profile`, `score-candidate`, `select-turn-order`, `weigh-bid`, `resolve-tie`, `admit-participant`, `choose-next-step`, `shape-fanout`, `classify-effect-risk` |  |
| [`select-llm-payload`](#def-select-llm-payload) | object |  |
| [`policy-hook-payload`](#def-policy-hook-payload) | object |  |
| [`digest`](#def-digest) | string |  |
| [`ref`](#def-ref) | string |  |
| [`text`](#def-text) | string |  |
| [`text-array`](#def-text-array) | array |  |
| [`candidate`](#def-candidate) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "hook/id": {
      "const": "select-llm-model"
    }
  },
  "required": [
    "hook/id"
  ]
}
```

Then:

```json
{
  "properties": {
    "hook/class": {
      "const": "select"
    },
    "payload": {
      "$ref": "#/$defs/select-llm-payload"
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "hook/id": {
      "enum": [
        "assemble-prompt",
        "score-candidate",
        "select-turn-order",
        "weigh-bid"
      ]
    }
  },
  "required": [
    "hook/id"
  ]
}
```

Then:

```json
{
  "properties": {
    "hook/class": {
      "const": "order"
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "hook/id": {
      "enum": [
        "select-output-schema",
        "resolve-tie",
        "choose-next-step"
      ]
    }
  },
  "required": [
    "hook/id"
  ]
}
```

Then:

```json
{
  "properties": {
    "hook/class": {
      "const": "select"
    }
  }
}
```

### Rule 4

When:

```json
{
  "properties": {
    "hook/id": {
      "const": "select-repair-profile"
    }
  },
  "required": [
    "hook/id"
  ]
}
```

Then:

```json
{
  "properties": {
    "hook/class": {
      "const": "select-profile"
    }
  }
}
```

### Rule 5

When:

```json
{
  "properties": {
    "hook/id": {
      "const": "admit-participant"
    }
  },
  "required": [
    "hook/id"
  ]
}
```

Then:

```json
{
  "properties": {
    "hook/class": {
      "const": "restrict"
    }
  }
}
```

### Rule 6

When:

```json
{
  "properties": {
    "hook/id": {
      "const": "shape-fanout"
    }
  },
  "required": [
    "hook/id"
  ]
}
```

Then:

```json
{
  "properties": {
    "hook/class": {
      "const": "narrow"
    }
  }
}
```

### Rule 7

When:

```json
{
  "properties": {
    "hook/id": {
      "const": "classify-effect-risk"
    }
  },
  "required": [
    "hook/id"
  ]
}
```

Then:

```json
{
  "properties": {
    "hook/class": {
      "const": "raise-risk"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nse-hook-offer.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-invocation-ref"></a>
## `invocation/ref`

- Required: `yes`
- Shape: string

<a id="field-hook-id"></a>
## `hook/id`

- Required: `yes`
- Shape: ref: `#/$defs/hook-id`

<a id="field-hook-v"></a>
## `hook/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-hook-class"></a>
## `hook/class`

- Required: `yes`
- Shape: enum: `select`, `order`, `narrow`, `restrict`, `raise-risk`, `select-profile`

<a id="field-offer-digest"></a>
## `offer/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-causal-ref"></a>
## `causal/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-backend-bounds"></a>
## `backend/bounds`

- Required: `yes`
- Shape: object

<a id="field-payload"></a>
## `payload`

- Required: `yes`
- Shape: unspecified

## Definition Semantics

<a id="def-hook-id"></a>
## `$defs.hook-id`

- Shape: enum: `select-llm-model`, `assemble-prompt`, `select-output-schema`, `select-repair-profile`, `score-candidate`, `select-turn-order`, `weigh-bid`, `resolve-tie`, `admit-participant`, `choose-next-step`, `shape-fanout`, `classify-effect-risk`

<a id="def-select-llm-payload"></a>
## `$defs.select-llm-payload`

- Shape: object

<a id="def-policy-hook-payload"></a>
## `$defs.policy-hook-payload`

- Shape: object

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-text"></a>
## `$defs.text`

- Shape: string

<a id="def-text-array"></a>
## `$defs.text-array`

- Shape: array

<a id="def-candidate"></a>
## `$defs.candidate`

- Shape: object
