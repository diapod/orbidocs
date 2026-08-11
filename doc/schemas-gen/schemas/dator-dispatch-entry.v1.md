# Dator Dispatch Entry v1

Source schema: [`doc/schemas/dator-dispatch-entry.v1.schema.json`](../../schemas/dator-dispatch-entry.v1.schema.json)

Domain-owned code-backed Dator dispatch adapter entry.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`entry/ref`](#field-entry-ref) | `yes` | string |  |
| [`entry/revision`](#field-entry-revision) | `yes` | integer |  |
| [`implementation/ref`](#field-implementation-ref) | `yes` | string |  |
| [`request/schema-ref`](#field-request-schema-ref) | `yes` | ref: `#/$defs/id` |  |
| [`response/schema-ref`](#field-response-schema-ref) | `yes` | ref: `#/$defs/id` |  |
| [`required/capability-ids`](#field-required-capability-ids) | `yes` | array |  |
| [`constraints`](#field-constraints) | `yes` | object |  |
| [`provenance`](#field-provenance) | `yes` | enum: `distribution-default`, `operator-package` |  |
| [`package/ref`](#field-package-ref) | `no` | ref: `#/$defs/id` |  |
| [`digest`](#field-digest) | `yes` | ref: `#/$defs/digest` |  |

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
    "package/ref"
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
      "package/ref"
    ]
  }
}
```

## Field Semantics

<a id="field-entry-ref"></a>
## `entry/ref`

- Required: `yes`
- Shape: string

<a id="field-entry-revision"></a>
## `entry/revision`

- Required: `yes`
- Shape: integer

<a id="field-implementation-ref"></a>
## `implementation/ref`

- Required: `yes`
- Shape: string

<a id="field-request-schema-ref"></a>
## `request/schema-ref`

- Required: `yes`
- Shape: ref: `#/$defs/id`

<a id="field-response-schema-ref"></a>
## `response/schema-ref`

- Required: `yes`
- Shape: ref: `#/$defs/id`

<a id="field-required-capability-ids"></a>
## `required/capability-ids`

- Required: `yes`
- Shape: array

<a id="field-constraints"></a>
## `constraints`

- Required: `yes`
- Shape: object

<a id="field-provenance"></a>
## `provenance`

- Required: `yes`
- Shape: enum: `distribution-default`, `operator-package`

<a id="field-package-ref"></a>
## `package/ref`

- Required: `no`
- Shape: ref: `#/$defs/id`

<a id="field-digest"></a>
## `digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

## Definition Semantics

<a id="def-id"></a>
## `$defs.id`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string
