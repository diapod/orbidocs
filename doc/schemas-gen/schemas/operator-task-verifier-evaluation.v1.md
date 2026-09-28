# Operator Task Verifier Evaluation v1

Source schema: [`doc/schemas/operator-task-verifier-evaluation.v1.schema.json`](../../schemas/operator-task-verifier-evaluation.v1.schema.json)

The host's judgment of one verifier result for one run: the exact verifier and result digests, each declared check as reported, and any check missing or unexpected. A run is verified only when every declared check is reported exactly once and passes; a failing check makes it `verification-failed`; a missing or unexpected check, a result outside the contracts, a timeout or a detected mutation refuses success with its code.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-verifier-evaluation.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`run/ref`](#field-run-ref) | `yes` | unspecified |  |
| [`verifier/ref`](#field-verifier-ref) | `yes` | unspecified |  |
| [`verifier/digest`](#field-verifier-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`result/ref`](#field-result-ref) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`result/digest`](#field-result-digest) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`checks`](#field-checks) | `yes` | array |  |
| [`passed`](#field-passed) | `yes` | boolean |  |
| [`refusal/code`](#field-refusal-code) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/refusalCode` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`check`](#def-check) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "refusal/code"
  ]
}
```

Then:

```json
{
  "properties": {
    "passed": {
      "const": false
    }
  }
}
```

### Rule 2

Constraint:

```json
{
  "dependentRequired": {
    "result/ref": [
      "result/digest"
    ],
    "result/digest": [
      "result/ref"
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-verifier-evaluation.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-run-ref"></a>
## `run/ref`

- Required: `yes`
- Shape: unspecified

<a id="field-verifier-ref"></a>
## `verifier/ref`

- Required: `yes`
- Shape: unspecified

<a id="field-verifier-digest"></a>
## `verifier/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-result-ref"></a>
## `result/ref`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-result-digest"></a>
## `result/digest`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-checks"></a>
## `checks`

- Required: `yes`
- Shape: array

<a id="field-passed"></a>
## `passed`

- Required: `yes`
- Shape: boolean

<a id="field-refusal-code"></a>
## `refusal/code`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/refusalCode`

## Definition Semantics

<a id="def-check"></a>
## `$defs.check`

- Shape: object
