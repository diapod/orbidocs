# Corpus Authority Epoch v1

Source schema: [`doc/schemas/corpus-authority-epoch.v1.schema.json`](../../schemas/corpus-authority-epoch.v1.schema.json)

Node-signed, communication-only continuation of the same logical round into a new immutable query/Room context. This is not membership or execution authority. The owner must resolve the original admitted source, exact historical bytes and provenance, current local mandate, chain head and cumulative budget. JSON Schema checks shape; the pure core checks content identity, signature, time interval and chain relations. No VM, HIL, lease or publication consent is inherited.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-authority-epoch.v1` |  |
| [`epoch/ref`](#field-epoch-ref) | `yes` | ref: `#/$defs/epoch-ref` |  |
| [`epoch/no`](#field-epoch-no) | `yes` | integer |  |
| [`origin`](#field-origin) | `yes` | ref: `#/$defs/origin` |  |
| [`previous/epoch-ref`](#field-previous-epoch-ref) | `no` | ref: `#/$defs/epoch-ref` |  |
| [`context`](#field-context) | `yes` | ref: `#/$defs/context` |  |
| [`chair/mandate`](#field-chair-mandate) | `yes` | unspecified |  |
| [`grants`](#field-grants) | `yes` | const: `['answer', 'observe', 'speak']` |  |
| [`retained/inputs`](#field-retained-inputs) | `yes` | array |  |
| [`created/at`](#field-created-at) | `yes` | string |  |
| [`valid/until`](#field-valid-until) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`query`](#def-query) | string |  |
| [`room`](#def-room) | string |  |
| [`digest`](#def-digest) | string |  |
| [`epoch-ref`](#def-epoch-ref) | string |  |
| [`context`](#def-context) | object |  |
| [`origin`](#def-origin) | object |  |
| [`input`](#def-input) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "epoch/no"
  ],
  "properties": {
    "epoch/no": {
      "const": 1
    }
  }
}
```

Then:

```json
{
  "not": {
    "required": [
      "previous/epoch-ref"
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-authority-epoch.v1`

<a id="field-epoch-ref"></a>
## `epoch/ref`

- Required: `yes`
- Shape: ref: `#/$defs/epoch-ref`

<a id="field-epoch-no"></a>
## `epoch/no`

- Required: `yes`
- Shape: integer

<a id="field-origin"></a>
## `origin`

- Required: `yes`
- Shape: ref: `#/$defs/origin`

<a id="field-previous-epoch-ref"></a>
## `previous/epoch-ref`

- Required: `no`
- Shape: ref: `#/$defs/epoch-ref`

<a id="field-context"></a>
## `context`

- Required: `yes`
- Shape: ref: `#/$defs/context`

<a id="field-chair-mandate"></a>
## `chair/mandate`

- Required: `yes`
- Shape: unspecified

<a id="field-grants"></a>
## `grants`

- Required: `yes`
- Shape: const: `['answer', 'observe', 'speak']`

<a id="field-retained-inputs"></a>
## `retained/inputs`

- Required: `yes`
- Shape: array

<a id="field-created-at"></a>
## `created/at`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid/until`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-query"></a>
## `$defs.query`

- Shape: string

<a id="def-room"></a>
## `$defs.room`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-epoch-ref"></a>
## `$defs.epoch-ref`

- Shape: string

<a id="def-context"></a>
## `$defs.context`

- Shape: object

<a id="def-origin"></a>
## `$defs.origin`

- Shape: object

<a id="def-input"></a>
## `$defs.input`

- Shape: object
