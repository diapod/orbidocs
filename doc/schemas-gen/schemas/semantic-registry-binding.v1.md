# Semantic Registry Binding v1

Source schema: [`doc/schemas/semantic-registry-binding.v1.schema.json`](../../schemas/semantic-registry-binding.v1.schema.json)

Exact activation binding for one domain-owned semantic registry entry.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `semantic-registry-binding.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`domain`](#field-domain) | `yes` | ref: `#/$defs/id` |  |
| [`entry/ref`](#field-entry-ref) | `yes` | ref: `#/$defs/id` |  |
| [`entry/revision`](#field-entry-revision) | `yes` | integer |  |
| [`implementation/ref`](#field-implementation-ref) | `yes` | ref: `#/$defs/id` |  |
| [`entry/digest`](#field-entry-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `no` | string |  |
| [`activation/generation`](#field-activation-generation) | `yes` | integer |  |
| [`provenance`](#field-provenance) | `yes` | enum: `distribution-default`, `operator-package` |  |
| [`activated-at`](#field-activated-at) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`id`](#def-id) | string |  |
| [`digest`](#def-digest) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "provenance": {
      "const": "operator-package"
    }
  },
  "required": [
    "provenance"
  ]
}
```

Then:

```json
{
  "required": [
    "operator/binding-ref"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "provenance": {
      "const": "distribution-default"
    }
  },
  "required": [
    "provenance"
  ]
}
```

Then:

```json
{
  "not": {
    "required": [
      "operator/binding-ref"
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `semantic-registry-binding.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-domain"></a>
## `domain`

- Required: `yes`
- Shape: ref: `#/$defs/id`

<a id="field-entry-ref"></a>
## `entry/ref`

- Required: `yes`
- Shape: ref: `#/$defs/id`

<a id="field-entry-revision"></a>
## `entry/revision`

- Required: `yes`
- Shape: integer

<a id="field-implementation-ref"></a>
## `implementation/ref`

- Required: `yes`
- Shape: ref: `#/$defs/id`

<a id="field-entry-digest"></a>
## `entry/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `no`
- Shape: string

<a id="field-activation-generation"></a>
## `activation/generation`

- Required: `yes`
- Shape: integer

<a id="field-provenance"></a>
## `provenance`

- Required: `yes`
- Shape: enum: `distribution-default`, `operator-package`

<a id="field-activated-at"></a>
## `activated-at`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-id"></a>
## `$defs.id`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string
