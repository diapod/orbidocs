# Corpus Thematic Profile v1

Source schema: [`doc/schemas/corpus-thematic-profile.v1.schema.json`](../../schemas/corpus-thematic-profile.v1.schema.json)

Optional exact-revision semantic-registry entry. Signed package or distribution authentication and receiving-host admission are prerequisites, not assertions made by this entry.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`entry/ref`](#field-entry-ref) | `yes` | unspecified |  |
| [`entry/revision`](#field-entry-revision) | `yes` | ref: `corpus-semantic-entry.v1.schema.json#/properties/entry~1revision` |  |
| [`implementation/ref`](#field-implementation-ref) | `yes` | ref: `corpus-semantic-entry.v1.schema.json#/$defs/id` |  |
| [`request/schema-ref`](#field-request-schema-ref) | `yes` | ref: `corpus-semantic-entry.v1.schema.json#/properties/request~1schema-ref` |  |
| [`response/schema-ref`](#field-response-schema-ref) | `yes` | ref: `corpus-semantic-entry.v1.schema.json#/properties/response~1schema-ref` |  |
| [`required/capability-ids`](#field-required-capability-ids) | `yes` | ref: `corpus-semantic-entry.v1.schema.json#/properties/required~1capability-ids` |  |
| [`provenance`](#field-provenance) | `yes` | ref: `corpus-semantic-entry.v1.schema.json#/properties/provenance` |  |
| [`package/ref`](#field-package-ref) | `no` | ref: `corpus-semantic-entry.v1.schema.json#/properties/package~1ref` |  |
| [`digest`](#field-digest) | `yes` | ref: `corpus-semantic-entry.v1.schema.json#/$defs/digest` |  |
| [`constraints`](#field-constraints) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`revision`](#def-revision) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "provenance"
  ],
  "properties": {
    "provenance": {
      "const": "operator-package"
    }
  }
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
  "required": [
    "provenance"
  ],
  "properties": {
    "provenance": {
      "const": "distribution-default"
    }
  }
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
- Shape: unspecified

<a id="field-entry-revision"></a>
## `entry/revision`

- Required: `yes`
- Shape: ref: `corpus-semantic-entry.v1.schema.json#/properties/entry~1revision`

<a id="field-implementation-ref"></a>
## `implementation/ref`

- Required: `yes`
- Shape: ref: `corpus-semantic-entry.v1.schema.json#/$defs/id`

<a id="field-request-schema-ref"></a>
## `request/schema-ref`

- Required: `yes`
- Shape: ref: `corpus-semantic-entry.v1.schema.json#/properties/request~1schema-ref`

<a id="field-response-schema-ref"></a>
## `response/schema-ref`

- Required: `yes`
- Shape: ref: `corpus-semantic-entry.v1.schema.json#/properties/response~1schema-ref`

<a id="field-required-capability-ids"></a>
## `required/capability-ids`

- Required: `yes`
- Shape: ref: `corpus-semantic-entry.v1.schema.json#/properties/required~1capability-ids`

<a id="field-provenance"></a>
## `provenance`

- Required: `yes`
- Shape: ref: `corpus-semantic-entry.v1.schema.json#/properties/provenance`

<a id="field-package-ref"></a>
## `package/ref`

- Required: `no`
- Shape: ref: `corpus-semantic-entry.v1.schema.json#/properties/package~1ref`

<a id="field-digest"></a>
## `digest`

- Required: `yes`
- Shape: ref: `corpus-semantic-entry.v1.schema.json#/$defs/digest`

<a id="field-constraints"></a>
## `constraints`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-revision"></a>
## `$defs.revision`

- Shape: object
