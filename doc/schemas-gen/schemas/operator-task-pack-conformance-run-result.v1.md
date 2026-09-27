# Operator Task Pack Conformance Run Result v1

Source schema: [`doc/schemas/operator-task-pack-conformance-run-result.v1.schema.json`](../../schemas/operator-task-pack-conformance-run-result.v1.schema.json)

Outcome of one task-pack conformance run: the recorded pack-facts evidence of each bound profile and, when every profile passed, the P085 conformance report the host recorded. A failed run records its evidence and no report.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-pack-conformance-run-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`package/ref`](#field-package-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`status`](#field-status) | `yes` | enum: `passed`, `failed` |  |
| [`profiles`](#field-profiles) | `yes` | array |  |
| [`package-report`](#field-package-report) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "const": "passed"
    }
  }
}
```

Then:

```json
{
  "required": [
    "package-report"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "status": {
      "const": "failed"
    }
  }
}
```

Then:

```json
{
  "not": {
    "required": [
      "package-report"
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-pack-conformance-run-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-package-ref"></a>
## `package/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `passed`, `failed`

<a id="field-profiles"></a>
## `profiles`

- Required: `yes`
- Shape: array

<a id="field-package-report"></a>
## `package-report`

- Required: `no`
- Shape: object
