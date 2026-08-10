# Operator Extension Safe Mode Action V1

Source schema: [`doc/schemas/operator-extension-safe-mode-action.v1.schema.json`](../../schemas/operator-extension-safe-mode-action.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-extension-safe-mode-action.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`action`](#field-action) | `yes` | enum: `enter`, `revoke-session-activations`, `deactivate-package`, `deactivate-all`, `restore-distribution-defaults`, `rebuild-projection`, `exit` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`package/ref`](#field-package-ref) | `no` | unspecified |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "action": {
      "const": "deactivate-package"
    }
  }
}
```

Then:

```json
{
  "required": [
    "package/ref"
  ],
  "properties": {
    "package/ref": {
      "$ref": "#/$defs/ref"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-extension-safe-mode-action.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-action"></a>
## `action`

- Required: `yes`
- Shape: enum: `enter`, `revoke-session-activations`, `deactivate-package`, `deactivate-all`, `restore-distribution-defaults`, `rebuild-projection`, `exit`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-package-ref"></a>
## `package/ref`

- Required: `no`
- Shape: unspecified

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
