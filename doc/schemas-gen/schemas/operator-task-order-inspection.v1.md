# Operator Task Order Inspection v1

Source schema: [`doc/schemas/operator-task-order-inspection.v1.schema.json`](../../schemas/operator-task-order-inspection.v1.schema.json)

Local read model of one Dator-admitted order and its explicit operator-selected round. A retained link grants no current loop, execution, Chair or HIL authority. Blocked may retain a historical link; it never removes source evidence.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-order-inspection.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`order/ref`](#field-order-ref) | `yes` | ref: `operator-task-order-link.request.v1.schema.json#/properties/order~1ref` |  |
| [`request/digest`](#field-request-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`selected-offer/digest`](#field-selected-offer-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`local-binding/current-digest`](#field-local-binding-current-digest) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`request`](#field-request) | `yes` | ref: `operator-task-order-input.v1.schema.json` |  |
| [`state`](#field-state) | `yes` | enum: `waiting-local-round`, `linked`, `blocked` |  |
| [`query/id`](#field-query-id) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`link/ref`](#field-link-ref) | `no` | string |  |
| [`delivery`](#field-delivery) | `no` | object | Read-only recovery state for an already committed result, separate from current order admissibility. Inspection does not register or retry delivery. The 24-hour BDO horizon never renews domain authority. |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "state"
  ],
  "properties": {
    "state": {
      "const": "linked"
    }
  }
}
```

Then:

```json
{
  "required": [
    "query/id",
    "link/ref",
    "local-binding/current-digest"
  ]
}
```

### Rule 2

When:

```json
{
  "required": [
    "state"
  ],
  "properties": {
    "state": {
      "const": "waiting-local-round"
    }
  }
}
```

Then:

```json
{
  "required": [
    "local-binding/current-digest"
  ],
  "not": {
    "anyOf": [
      {
        "required": [
          "link/ref"
        ]
      },
      {
        "required": [
          "query/id"
        ]
      }
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-order-inspection.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-order-ref"></a>
## `order/ref`

- Required: `yes`
- Shape: ref: `operator-task-order-link.request.v1.schema.json#/properties/order~1ref`

<a id="field-request-digest"></a>
## `request/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-selected-offer-digest"></a>
## `selected-offer/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-local-binding-current-digest"></a>
## `local-binding/current-digest`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-request"></a>
## `request`

- Required: `yes`
- Shape: ref: `operator-task-order-input.v1.schema.json`

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `waiting-local-round`, `linked`, `blocked`

<a id="field-query-id"></a>
## `query/id`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-link-ref"></a>
## `link/ref`

- Required: `no`
- Shape: string

<a id="field-delivery"></a>
## `delivery`

- Required: `no`
- Shape: object

Read-only recovery state for an already committed result, separate from current order admissibility. Inspection does not register or retry delivery. The 24-hour BDO horizon never renews domain authority.
