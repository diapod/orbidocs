# NSE Hook Decision Proposal v1

Source schema: [`doc/schemas/nse-hook-decision.v1.schema.json`](../../schemas/nse-hook-decision.v1.schema.json)

Raw producer proposal bound to one exact NSE offer. Admission remains host-owned.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nse-hook-decision.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`invocation/ref`](#field-invocation-ref) | `yes` | string |  |
| [`hook/id`](#field-hook-id) | `yes` | ref: `#/$defs/hook-id` |  |
| [`hook/v`](#field-hook-v) | `yes` | const: `1` |  |
| [`offer/digest`](#field-offer-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`producer/ref`](#field-producer-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`producer/digest`](#field-producer-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`outcome`](#field-outcome) | `yes` | unspecified |  |
| [`annotations`](#field-annotations) | `no` | ref: `#/$defs/annotations` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`hook-id`](#def-hook-id) | enum: `select-llm-model`, `assemble-prompt`, `select-output-schema`, `select-repair-profile`, `score-candidate`, `select-turn-order`, `weigh-bid`, `resolve-tie`, `admit-participant`, `choose-next-step`, `shape-fanout`, `classify-effect-risk` |  |
| [`select-llm-decision`](#def-select-llm-decision) | object |  |
| [`policy-hook-decision`](#def-policy-hook-decision) | object |  |
| [`select-outcome`](#def-select-outcome) | object |  |
| [`order-outcome`](#def-order-outcome) | object |  |
| [`narrow-outcome`](#def-narrow-outcome) | object |  |
| [`restrict-outcome`](#def-restrict-outcome) | object |  |
| [`raise-risk-outcome`](#def-raise-risk-outcome) | object |  |
| [`select-profile-outcome`](#def-select-profile-outcome) | object |  |
| [`defer-outcome`](#def-defer-outcome) | object |  |
| [`refs`](#def-refs) | array |  |
| [`limits`](#def-limits) | object |  |
| [`digest`](#def-digest) | string |  |
| [`ref`](#def-ref) | string |  |
| [`text`](#def-text) | string |  |
| [`reason`](#def-reason) | object |  |
| [`use-runtime`](#def-use-runtime) | object |  |
| [`annotations`](#def-annotations) | object |  |

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
    "outcome": {
      "$ref": "#/$defs/select-llm-decision"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nse-hook-decision.v1`

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

<a id="field-offer-digest"></a>
## `offer/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-producer-ref"></a>
## `producer/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-producer-digest"></a>
## `producer/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: unspecified

<a id="field-annotations"></a>
## `annotations`

- Required: `no`
- Shape: ref: `#/$defs/annotations`

## Definition Semantics

<a id="def-hook-id"></a>
## `$defs.hook-id`

- Shape: enum: `select-llm-model`, `assemble-prompt`, `select-output-schema`, `select-repair-profile`, `score-candidate`, `select-turn-order`, `weigh-bid`, `resolve-tie`, `admit-participant`, `choose-next-step`, `shape-fanout`, `classify-effect-risk`

<a id="def-select-llm-decision"></a>
## `$defs.select-llm-decision`

- Shape: object

<a id="def-policy-hook-decision"></a>
## `$defs.policy-hook-decision`

- Shape: object

<a id="def-select-outcome"></a>
## `$defs.select-outcome`

- Shape: object

<a id="def-order-outcome"></a>
## `$defs.order-outcome`

- Shape: object

<a id="def-narrow-outcome"></a>
## `$defs.narrow-outcome`

- Shape: object

<a id="def-restrict-outcome"></a>
## `$defs.restrict-outcome`

- Shape: object

<a id="def-raise-risk-outcome"></a>
## `$defs.raise-risk-outcome`

- Shape: object

<a id="def-select-profile-outcome"></a>
## `$defs.select-profile-outcome`

- Shape: object

<a id="def-defer-outcome"></a>
## `$defs.defer-outcome`

- Shape: object

<a id="def-refs"></a>
## `$defs.refs`

- Shape: array

<a id="def-limits"></a>
## `$defs.limits`

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

<a id="def-reason"></a>
## `$defs.reason`

- Shape: object

<a id="def-use-runtime"></a>
## `$defs.use-runtime`

- Shape: object

<a id="def-annotations"></a>
## `$defs.annotations`

- Shape: object
