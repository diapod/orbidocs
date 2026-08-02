# Operator Resource Envelope v1

Source schema: [`doc/schemas/operator-resource-envelope.v1.schema.json`](../../schemas/operator-resource-envelope.v1.schema.json)

Signed append-only operator revision binding one organ-owned typed resource profile. It bounds already-authorized work and grants no capability or effect authority.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-resource-envelope.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`envelope/id`](#field-envelope-id) | `yes` | ref: `#/$defs/envelope-ref` |  |
| [`revision/no`](#field-revision-no) | `yes` | integer |  |
| [`supersedes/ref`](#field-supersedes-ref) | `no` | ref: `#/$defs/envelope-ref` |  |
| [`scope`](#field-scope) | `yes` | object |  |
| [`experiment/classes`](#field-experiment-classes) | `yes` | array |  |
| [`profile/schema`](#field-profile-schema) | `yes` | const: `inquirium-resource-profile.v1` |  |
| [`profile/digest`](#field-profile-digest) | `yes` | ref: `#/$defs/hex-digest` |  |
| [`profile`](#field-profile) | `yes` | ref: `inquirium-resource-profile.v1.schema.json` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | string |  |
| [`reason`](#field-reason) | `yes` | string |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`token`](#def-token) | string |  |
| [`envelope-ref`](#def-envelope-ref) | string |  |
| [`hex-digest`](#def-hex-digest) | string |  |
| [`signature`](#def-signature) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "revision/no": {
      "const": 1
    }
  },
  "required": [
    "revision/no"
  ]
}
```

Then:

```json
{
  "not": {
    "required": [
      "supersedes/ref"
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-resource-envelope.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-envelope-id"></a>
## `envelope/id`

- Required: `yes`
- Shape: ref: `#/$defs/envelope-ref`

<a id="field-revision-no"></a>
## `revision/no`

- Required: `yes`
- Shape: integer

<a id="field-supersedes-ref"></a>
## `supersedes/ref`

- Required: `no`
- Shape: ref: `#/$defs/envelope-ref`

<a id="field-scope"></a>
## `scope`

- Required: `yes`
- Shape: object

<a id="field-experiment-classes"></a>
## `experiment/classes`

- Required: `yes`
- Shape: array

<a id="field-profile-schema"></a>
## `profile/schema`

- Required: `yes`
- Shape: const: `inquirium-resource-profile.v1`

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: ref: `#/$defs/hex-digest`

<a id="field-profile"></a>
## `profile`

- Required: `yes`
- Shape: ref: `inquirium-resource-profile.v1.schema.json`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: string

<a id="field-reason"></a>
## `reason`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

## Definition Semantics

<a id="def-token"></a>
## `$defs.token`

- Shape: string

<a id="def-envelope-ref"></a>
## `$defs.envelope-ref`

- Shape: string

<a id="def-hex-digest"></a>
## `$defs.hex-digest`

- Shape: string

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
