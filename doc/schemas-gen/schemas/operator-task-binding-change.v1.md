# Operator Task Binding Change v1

Source schema: [`doc/schemas/operator-task-binding-change.v1.schema.json`](../../schemas/operator-task-binding-change.v1.schema.json)

Audit fact of an authorized local-binding change attempt: which binding, what kind of change, the verified actor, and the proposed binding revision before and after it, as `local-binding/digest` values. An ordinary change names the verified operator participant and operator binding; an emergency pause names the host-local channel and no operator. The fact is written before the binding, so a change without its fact never takes effect. If the binding write fails, the fact remains an attempt, not standalone proof of commit or authority to replay. It carries no profile content, local paths or secrets.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-binding-change.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`change/kind`](#field-change-kind) | `yes` | enum: `create`, `pause`, `resume`, `accept-profile`, `emergency-pause` |  |
| [`actor`](#field-actor) | `yes` | object |  |
| [`local-binding/previous-digest`](#field-local-binding-previous-digest) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`local-binding/digest`](#field-local-binding-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`recorded-at`](#field-recorded-at) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/timestamp` |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "change/kind": {
      "const": "create"
    }
  },
  "required": [
    "change/kind"
  ]
}
```

Then:

```json
{
  "not": {
    "required": [
      "local-binding/previous-digest"
    ]
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "change/kind": {
      "const": "emergency-pause"
    }
  },
  "required": [
    "change/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "actor": {
      "properties": {
        "actor/kind": {
          "const": "host-local"
        }
      }
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-binding-change.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-change-kind"></a>
## `change/kind`

- Required: `yes`
- Shape: enum: `create`, `pause`, `resume`, `accept-profile`, `emergency-pause`

<a id="field-actor"></a>
## `actor`

- Required: `yes`
- Shape: object

<a id="field-local-binding-previous-digest"></a>
## `local-binding/previous-digest`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-local-binding-digest"></a>
## `local-binding/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-recorded-at"></a>
## `recorded-at`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/timestamp`
