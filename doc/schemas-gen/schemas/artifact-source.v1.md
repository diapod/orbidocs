# Artifact Source v1

Source schema: [`doc/schemas/artifact-source.v1.schema.json`](../../schemas/artifact-source.v1.schema.json)

Immutable operator-owned declaration for one read-only artifact source generation. Locators contain references or public URLs, never credential values or executable paths.

## Governing Basis

- [`doc/project/40-proposals/088-pull-based-artifact-acquisition.md`](../../project/40-proposals/088-pull-based-artifact-acquisition.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `artifact-source.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`source/id`](#field-source-id) | `yes` | string |  |
| [`source/generation`](#field-source-generation) | `yes` | integer |  |
| [`connector/id`](#field-connector-id) | `yes` | string |  |
| [`locator`](#field-locator) | `yes` | ref: `#/$defs/locator` |  |
| [`credential/ref`](#field-credential-ref) | `no` | ref: `#/$defs/ref` |  |
| [`trigger/modes`](#field-trigger-modes) | `yes` | array |  |
| [`allow`](#field-allow) | `yes` | ref: `#/$defs/allow` |  |
| [`extraction`](#field-extraction) | `yes` | ref: `#/$defs/extraction` |  |
| [`admission/mode`](#field-admission-mode) | `yes` | enum: `stage`, `admit-known` |  |
| [`admission/table-ref`](#field-admission-table-ref) | `no` | ref: `#/$defs/ref` |  |
| [`limits`](#field-limits) | `yes` | ref: `#/$defs/limits` |  |
| [`freshness/max-staleness-seconds`](#field-freshness-max-staleness-seconds) | `yes` | integer |  |
| [`consumption/mode`](#field-consumption-mode) | `yes` | const: `read-only` |  |
| [`checkpoint/policy`](#field-checkpoint-policy) | `no` | enum: `none`, `generation-bound` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`ref`](#def-ref) | string |  |
| [`locator`](#def-locator) | unspecified |  |
| [`allow`](#def-allow) | object |  |
| [`nonEmptyStringSet`](#def-nonemptystringset) | array |  |
| [`extraction`](#def-extraction) | object |  |
| [`limits`](#def-limits) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "admission/mode": {
      "const": "admit-known"
    }
  }
}
```

Then:

```json
{
  "required": [
    "admission/table-ref"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `artifact-source.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-source-id"></a>
## `source/id`

- Required: `yes`
- Shape: string

<a id="field-source-generation"></a>
## `source/generation`

- Required: `yes`
- Shape: integer

<a id="field-connector-id"></a>
## `connector/id`

- Required: `yes`
- Shape: string

<a id="field-locator"></a>
## `locator`

- Required: `yes`
- Shape: ref: `#/$defs/locator`

<a id="field-credential-ref"></a>
## `credential/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-trigger-modes"></a>
## `trigger/modes`

- Required: `yes`
- Shape: array

<a id="field-allow"></a>
## `allow`

- Required: `yes`
- Shape: ref: `#/$defs/allow`

<a id="field-extraction"></a>
## `extraction`

- Required: `yes`
- Shape: ref: `#/$defs/extraction`

<a id="field-admission-mode"></a>
## `admission/mode`

- Required: `yes`
- Shape: enum: `stage`, `admit-known`

<a id="field-admission-table-ref"></a>
## `admission/table-ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: ref: `#/$defs/limits`

<a id="field-freshness-max-staleness-seconds"></a>
## `freshness/max-staleness-seconds`

- Required: `yes`
- Shape: integer

<a id="field-consumption-mode"></a>
## `consumption/mode`

- Required: `yes`
- Shape: const: `read-only`

<a id="field-checkpoint-policy"></a>
## `checkpoint/policy`

- Required: `no`
- Shape: enum: `none`, `generation-bound`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-locator"></a>
## `$defs.locator`

- Shape: unspecified

<a id="def-allow"></a>
## `$defs.allow`

- Shape: object

<a id="def-nonemptystringset"></a>
## `$defs.nonEmptyStringSet`

- Shape: array

<a id="def-extraction"></a>
## `$defs.extraction`

- Shape: object

<a id="def-limits"></a>
## `$defs.limits`

- Shape: object
