# Exact Owner-resolved Communication Epoch Preview v1

Source schema: [`doc/schemas/corpus-authority-epoch.preview.v1.schema.json`](../../schemas/corpus-authority-epoch.preview.v1.schema.json)

Separate approval binds the immutable logical origin, current predecessor, communication-only rights, fresh Room choices and exact inert historical inputs. This is not a membership receipt or experiment permit. The owner rechecks scope and current authority on commit.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-authority-epoch.preview.v1` |  |
| [`source/query-id`](#field-source-query-id) | `yes` | ref: `corpus-authority-epoch.v1.schema.json#/$defs/query` |  |
| [`origin`](#field-origin) | `yes` | ref: `corpus-authority-epoch.v1.schema.json#/$defs/origin` |  |
| [`epoch/no`](#field-epoch-no) | `yes` | integer |  |
| [`previous/epoch-ref`](#field-previous-epoch-ref) | `no` | ref: `corpus-authority-epoch.v1.schema.json#/$defs/epoch-ref` |  |
| [`chair/mandate`](#field-chair-mandate) | `yes` | ref: `corpus-authority-epoch.v1.schema.json#/properties/chair~1mandate` |  |
| [`grants`](#field-grants) | `yes` | const: `['answer', 'observe', 'speak']` |  |
| [`retained/inputs`](#field-retained-inputs) | `yes` | ref: `corpus-authority-epoch.v1.schema.json#/properties/retained~1inputs` |  |
| [`created/at`](#field-created-at) | `yes` | string |  |
| [`valid/until`](#field-valid-until) | `yes` | string |  |
| [`round`](#field-round) | `yes` | ref: `corpus-local-round.preview.v1.schema.json` |  |

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
- Shape: const: `corpus-authority-epoch.preview.v1`

<a id="field-source-query-id"></a>
## `source/query-id`

- Required: `yes`
- Shape: ref: `corpus-authority-epoch.v1.schema.json#/$defs/query`

<a id="field-origin"></a>
## `origin`

- Required: `yes`
- Shape: ref: `corpus-authority-epoch.v1.schema.json#/$defs/origin`

<a id="field-epoch-no"></a>
## `epoch/no`

- Required: `yes`
- Shape: integer

<a id="field-previous-epoch-ref"></a>
## `previous/epoch-ref`

- Required: `no`
- Shape: ref: `corpus-authority-epoch.v1.schema.json#/$defs/epoch-ref`

<a id="field-chair-mandate"></a>
## `chair/mandate`

- Required: `yes`
- Shape: ref: `corpus-authority-epoch.v1.schema.json#/properties/chair~1mandate`

<a id="field-grants"></a>
## `grants`

- Required: `yes`
- Shape: const: `['answer', 'observe', 'speak']`

<a id="field-retained-inputs"></a>
## `retained/inputs`

- Required: `yes`
- Shape: ref: `corpus-authority-epoch.v1.schema.json#/properties/retained~1inputs`

<a id="field-created-at"></a>
## `created/at`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid/until`

- Required: `yes`
- Shape: string

<a id="field-round"></a>
## `round`

- Required: `yes`
- Shape: ref: `corpus-local-round.preview.v1.schema.json`
