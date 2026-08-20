# Agent Inference Flow Inspection v1

Source schema: [`doc/schemas/agent.inference-flow-inspection.v1.schema.json`](../../schemas/agent.inference-flow-inspection.v1.schema.json)

A bounded prompt-free operator projection for one Agent inference Flow.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)
- [`doc/project/60-solutions/047-agent/047-agent.md`](../../project/60-solutions/047-agent/047-agent.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.inference-flow-inspection.v1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`flow/ref`](#field-flow-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`flow/digest`](#field-flow-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`package/ref`](#field-package-ref) | `no` | ref: `#/$defs/ref` |  |
| [`package/digest`](#field-package-digest) | `no` | ref: `#/$defs/package-digest` |  |
| [`package/activation-generation`](#field-package-activation-generation) | `no` | integer |  |
| [`agent-policy/ref`](#field-agent-policy-ref) | `no` | ref: `#/$defs/ref` |  |
| [`agent-policy/digest`](#field-agent-policy-digest) | `no` | ref: `#/$defs/digest` |  |
| [`passages/used`](#field-passages-used) | `yes` | integer |  |
| [`passages/max`](#field-passages-max) | `yes` | integer |  |
| [`current/passage-ref`](#field-current-passage-ref) | `no` | ref: `#/$defs/ref` |  |
| [`current/state`](#field-current-state) | `no` | enum: `admitted`, `committed`, `refused`, `selected` |  |
| [`current/decision-code`](#field-current-decision-code) | `no` | enum: `passage-admitted`, `passage-committed`, `terminal-product-selected`, `passage-request-refused`, `passage-invocation-refused`, `passage-response-refused`, `passage-artifact-refused`, `passage-commit-refused` |  |
| [`decisive/restriction`](#field-decisive-restriction) | `no` | ref: `#/$defs/ref` |  |
| [`omitted-producer/refs`](#field-omitted-producer-refs) | `no` | array |  |
| [`parent-product/refs`](#field-parent-product-refs) | `yes` | array |  |
| [`prompt-policy/ref`](#field-prompt-policy-ref) | `no` | ref: `#/$defs/ref` |  |
| [`output-schema/ref`](#field-output-schema-ref) | `no` | ref: `#/$defs/ref` |  |
| [`repair-profile/ref`](#field-repair-profile-ref) | `no` | ref: `#/$defs/ref` |  |
| [`model-profile/ref`](#field-model-profile-ref) | `no` | ref: `#/$defs/ref` |  |
| [`runtime/ref`](#field-runtime-ref) | `no` | ref: `#/$defs/ref` |  |
| [`visibility/ceiling`](#field-visibility-ceiling) | `yes` | enum: `private`, `operator`, `shared` |  |
| [`terminal/product-ref`](#field-terminal-product-ref) | `no` | ref: `#/$defs/ref` |  |
| [`budget/spent`](#field-budget-spent) | `yes` | ref: `#/$defs/budget` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`package-digest`](#def-package-digest) | string |  |
| [`budget`](#def-budget) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "decisive/restriction"
  ]
}
```

Then:

```json
{
  "properties": {
    "current/state": {
      "const": "refused"
    }
  },
  "required": [
    "current/state"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.inference-flow-inspection.v1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-flow-ref"></a>
## `flow/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-flow-digest"></a>
## `flow/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-package-ref"></a>
## `package/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-package-digest"></a>
## `package/digest`

- Required: `no`
- Shape: ref: `#/$defs/package-digest`

<a id="field-package-activation-generation"></a>
## `package/activation-generation`

- Required: `no`
- Shape: integer

<a id="field-agent-policy-ref"></a>
## `agent-policy/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-agent-policy-digest"></a>
## `agent-policy/digest`

- Required: `no`
- Shape: ref: `#/$defs/digest`

<a id="field-passages-used"></a>
## `passages/used`

- Required: `yes`
- Shape: integer

<a id="field-passages-max"></a>
## `passages/max`

- Required: `yes`
- Shape: integer

<a id="field-current-passage-ref"></a>
## `current/passage-ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-current-state"></a>
## `current/state`

- Required: `no`
- Shape: enum: `admitted`, `committed`, `refused`, `selected`

<a id="field-current-decision-code"></a>
## `current/decision-code`

- Required: `no`
- Shape: enum: `passage-admitted`, `passage-committed`, `terminal-product-selected`, `passage-request-refused`, `passage-invocation-refused`, `passage-response-refused`, `passage-artifact-refused`, `passage-commit-refused`

<a id="field-decisive-restriction"></a>
## `decisive/restriction`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-omitted-producer-refs"></a>
## `omitted-producer/refs`

- Required: `no`
- Shape: array

<a id="field-parent-product-refs"></a>
## `parent-product/refs`

- Required: `yes`
- Shape: array

<a id="field-prompt-policy-ref"></a>
## `prompt-policy/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-output-schema-ref"></a>
## `output-schema/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-repair-profile-ref"></a>
## `repair-profile/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-model-profile-ref"></a>
## `model-profile/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-runtime-ref"></a>
## `runtime/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-visibility-ceiling"></a>
## `visibility/ceiling`

- Required: `yes`
- Shape: enum: `private`, `operator`, `shared`

<a id="field-terminal-product-ref"></a>
## `terminal/product-ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-budget-spent"></a>
## `budget/spent`

- Required: `yes`
- Shape: ref: `#/$defs/budget`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-package-digest"></a>
## `$defs.package-digest`

- Shape: string

<a id="def-budget"></a>
## `$defs.budget`

- Shape: object
