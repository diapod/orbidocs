# Orbiplex Acceptance Storage Policy v1

Source schema: [`doc/schemas/orbiplex-acceptance-storage-policy.v1.schema.json`](../../schemas/orbiplex-acceptance-storage-policy.v1.schema.json)

Host-local, run-scoped opt-in policy for shared or removable acceptance storage. This private import contract may contain local paths and principal ids and must not be retained in aggregate reports.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `orbiplex-acceptance-storage-policy.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`policy/ref`](#field-policy-ref) | `yes` | string |  |
| [`posture`](#field-posture) | `yes` | enum: `operator-authorized-shared`, `operator-trusted-shared-managed` |  |
| [`scope`](#field-scope) | `yes` | ref: `#/$defs/scope` |  |
| [`bindings`](#field-bindings) | `yes` | array |  |
| [`trust/assertion`](#field-trust-assertion) | `yes` | const: `trusted-non-adversarial` |  |
| [`risk/acknowledgement`](#field-risk-acknowledgement) | `no` | const: `shared-managed-toctou-v1` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`rawDigest`](#def-rawdigest) | string |  |
| [`token`](#def-token) | string |  |
| [`scope`](#def-scope) | object |  |
| [`binding`](#def-binding) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "posture": {
      "const": "operator-trusted-shared-managed"
    }
  },
  "required": [
    "posture"
  ]
}
```

Then:

```json
{
  "required": [
    "risk/acknowledgement"
  ],
  "properties": {
    "bindings": {
      "contains": {
        "properties": {
          "storage/role": {
            "const": "model-managed-store"
          }
        },
        "required": [
          "storage/role"
        ]
      }
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `orbiplex-acceptance-storage-policy.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `yes`
- Shape: string

<a id="field-posture"></a>
## `posture`

- Required: `yes`
- Shape: enum: `operator-authorized-shared`, `operator-trusted-shared-managed`

<a id="field-scope"></a>
## `scope`

- Required: `yes`
- Shape: ref: `#/$defs/scope`

<a id="field-bindings"></a>
## `bindings`

- Required: `yes`
- Shape: array

<a id="field-trust-assertion"></a>
## `trust/assertion`

- Required: `yes`
- Shape: const: `trusted-non-adversarial`

<a id="field-risk-acknowledgement"></a>
## `risk/acknowledgement`

- Required: `no`
- Shape: const: `shared-managed-toctou-v1`

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-rawdigest"></a>
## `$defs.rawDigest`

- Shape: string

<a id="def-token"></a>
## `$defs.token`

- Shape: string

<a id="def-scope"></a>
## `$defs.scope`

- Shape: object

<a id="def-binding"></a>
## `$defs.binding`

- Shape: object
