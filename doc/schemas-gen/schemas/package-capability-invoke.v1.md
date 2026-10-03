# Package Capability Invoke v1

Source schema: [`doc/schemas/package-capability-invoke.v1.schema.json`](../../schemas/package-capability-invoke.v1.schema.json)

One local invocation of a package capability (P093 §11, R13). `use-binding/ref` may name the approved use the caller acts under; the host attests the caller from its own session and records and never from this field. The request fingerprint covers `capability/id`, `contract/digest`, `issued-at`, `deadline` and `input`.

## Governing Basis

- [`doc/project/40-proposals/093-package-scoped-private-capabilities.md`](../../project/40-proposals/093-package-scoped-private-capabilities.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `package-capability-invoke.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`capability/id`](#field-capability-id) | `yes` | ref: `#/$defs/capability-id` |  |
| [`contract/digest`](#field-contract-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`invocation/id`](#field-invocation-id) | `yes` | ref: `#/$defs/invocation-id` |  |
| [`issued-at`](#field-issued-at) | `yes` | ref: `#/$defs/timestamp` |  |
| [`deadline`](#field-deadline) | `yes` | ref: `#/$defs/timestamp` |  |
| [`use-binding/ref`](#field-use-binding-ref) | `no` | ref: `#/$defs/ref` |  |
| [`input`](#field-input) | `yes` | unspecified | Validated by the host against the contract's input schema before the admission point. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`capability-id`](#def-capability-id) | string | A package capability identifier (P093 §2); the host parses it with the one grammar. |
| [`digest`](#def-digest) | string |  |
| [`invocation-id`](#def-invocation-id) | string |  |
| [`timestamp`](#def-timestamp) | string |  |
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `package-capability-invoke.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: ref: `#/$defs/capability-id`

<a id="field-contract-digest"></a>
## `contract/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-invocation-id"></a>
## `invocation/id`

- Required: `yes`
- Shape: ref: `#/$defs/invocation-id`

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: ref: `#/$defs/timestamp`

<a id="field-deadline"></a>
## `deadline`

- Required: `yes`
- Shape: ref: `#/$defs/timestamp`

<a id="field-use-binding-ref"></a>
## `use-binding/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-input"></a>
## `input`

- Required: `yes`
- Shape: unspecified

Validated by the host against the contract's input schema before the admission point.

## Definition Semantics

<a id="def-capability-id"></a>
## `$defs.capability-id`

- Shape: string

A package capability identifier (P093 §2); the host parses it with the one grammar.

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-invocation-id"></a>
## `$defs.invocation-id`

- Shape: string

<a id="def-timestamp"></a>
## `$defs.timestamp`

- Shape: string

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
