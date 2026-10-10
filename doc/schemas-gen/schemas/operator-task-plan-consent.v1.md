# Operator-task-plan-consent.v1

Source schema: [`doc/schemas/operator-task-plan-consent.v1.schema.json`](../../schemas/operator-task-plan-consent.v1.schema.json)

Approval of the complete exact immutable plan of ONE admitted run, including patch addresses. It cannot be reused for a second run. Delegation additionally requires a live signed loop mandate; rollback never requires live consent.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-plan-consent.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`run/ref`](#field-run-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`plan/ref`](#field-plan-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`plan/digest`](#field-plan-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`pins`](#field-pins) | `yes` | object |  |
| [`valid/until`](#field-valid-until) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/timestamp` |  |
| [`confirmation/mode`](#field-confirmation-mode) | `yes` | enum: `direct`, `delegated` |  |
| [`confirmation/ref`](#field-confirmation-ref) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`supersedes/digest`](#field-supersedes-digest) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/digest` | A new direct approval commits to the retained delegated consent. It preserves the same run, plan and pins, without replaying completed steps or renewing the mandate. |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "confirmation/mode"
  ],
  "properties": {
    "confirmation/mode": {
      "const": "delegated"
    }
  }
}
```

Then:

```json
{
  "required": [
    "confirmation/ref"
  ],
  "not": {
    "required": [
      "supersedes/digest"
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-plan-consent.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-run-ref"></a>
## `run/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-plan-ref"></a>
## `plan/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-plan-digest"></a>
## `plan/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-pins"></a>
## `pins`

- Required: `yes`
- Shape: object

<a id="field-valid-until"></a>
## `valid/until`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/timestamp`

<a id="field-confirmation-mode"></a>
## `confirmation/mode`

- Required: `yes`
- Shape: enum: `direct`, `delegated`

<a id="field-confirmation-ref"></a>
## `confirmation/ref`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-supersedes-digest"></a>
## `supersedes/digest`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

A new direct approval commits to the retained delegated consent. It preserves the same run, plan and pins, without replaying completed steps or renewing the mandate.
