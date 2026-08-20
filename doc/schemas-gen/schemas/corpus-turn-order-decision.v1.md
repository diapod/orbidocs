# Corpus Turn Order Decision v1

Source schema: [`doc/schemas/corpus-turn-order-decision.v1.schema.json`](../../schemas/corpus-turn-order-decision.v1.schema.json)

Prompt-free result of resolving one exact target-free Corpus turn-order offer; it is evidence, not Room authority.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-turn-order-decision.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`decision/ref`](#field-decision-ref) | `yes` | string |  |
| [`decision/digest`](#field-decision-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`offer/ref`](#field-offer-ref) | `yes` | string |  |
| [`offer/digest`](#field-offer-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`source`](#field-source) | `yes` | enum: `distribution-policy`, `operator-policy` |  |
| [`operator/authority-decision-ref`](#field-operator-authority-decision-ref) | `no` | string |  |
| [`ordered/candidate-refs`](#field-ordered-candidate-refs) | `yes` | array |  |
| [`selected/candidate-ref`](#field-selected-candidate-ref) | `yes` | ref: `#/$defs/candidate-ref` |  |
| [`decided-at`](#field-decided-at) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`candidate-ref`](#def-candidate-ref) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "source"
  ],
  "properties": {
    "source": {
      "const": "operator-policy"
    }
  }
}
```

Then:

```json
{
  "required": [
    "operator/authority-decision-ref"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-turn-order-decision.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-decision-ref"></a>
## `decision/ref`

- Required: `yes`
- Shape: string

<a id="field-decision-digest"></a>
## `decision/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-offer-ref"></a>
## `offer/ref`

- Required: `yes`
- Shape: string

<a id="field-offer-digest"></a>
## `offer/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-source"></a>
## `source`

- Required: `yes`
- Shape: enum: `distribution-policy`, `operator-policy`

<a id="field-operator-authority-decision-ref"></a>
## `operator/authority-decision-ref`

- Required: `no`
- Shape: string

<a id="field-ordered-candidate-refs"></a>
## `ordered/candidate-refs`

- Required: `yes`
- Shape: array

<a id="field-selected-candidate-ref"></a>
## `selected/candidate-ref`

- Required: `yes`
- Shape: ref: `#/$defs/candidate-ref`

<a id="field-decided-at"></a>
## `decided-at`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-candidate-ref"></a>
## `$defs.candidate-ref`

- Shape: string
