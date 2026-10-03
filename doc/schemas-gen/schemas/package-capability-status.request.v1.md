# Package Capability Status Request v1

Source schema: [`doc/schemas/package-capability-status.request.v1.schema.json`](../../schemas/package-capability-status.request.v1.schema.json)

A read-only status query of one invocation (P093 §13). It carries no input, is authorized like an invocation, reads only the host journal and never dispatches or reconciles.

## Governing Basis

- [`doc/project/40-proposals/093-package-scoped-private-capabilities.md`](../../project/40-proposals/093-package-scoped-private-capabilities.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `package-capability-status.request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`capability/id`](#field-capability-id) | `yes` | ref: `#/$defs/capability-id` |  |
| [`contract/digest`](#field-contract-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`invocation/id`](#field-invocation-id) | `yes` | ref: `#/$defs/invocation-id` |  |
| [`request/digest`](#field-request-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`use-binding/ref`](#field-use-binding-ref) | `no` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`capability-id`](#def-capability-id) | string | A package capability identifier (P093 §2); the host parses it with the one grammar. |
| [`digest`](#def-digest) | string |  |
| [`invocation-id`](#def-invocation-id) | string |  |
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `package-capability-status.request.v1`

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

<a id="field-request-digest"></a>
## `request/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-use-binding-ref"></a>
## `use-binding/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

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

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
