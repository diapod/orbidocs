# Package Capability Declaration v1

Source schema: [`doc/schemas/package-capability-declaration.v1.schema.json`](../../schemas/package-capability-declaration.v1.schema.json)

One behaviour a signed package provides under a package capability identifier (P093 §5). It names behaviour, never host authority: `requires/capabilities` must be a subset of the base capabilities the activation was granted. The provider is one host-managed component, identified by `provider.component/id` and the `provides[]` entry of its component contract; for an in-process JSON-e Flow the provider also pins the Flow id and the digest of its delivered source, which stay distinct from the capability id. Activation compares the identifier's anchor with the key that verified the package and the package name with `package/ref`; the declared value is never trusted as a label.

## Governing Basis

- [`doc/project/40-proposals/093-package-scoped-private-capabilities.md`](../../project/40-proposals/093-package-scoped-private-capabilities.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `package-capability-declaration.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`capability/id`](#field-capability-id) | `yes` | string | `name@scope-ns:did:key:z…/package`, read by the one capability identifier grammar. |
| [`capability/scope`](#field-capability-scope) | `yes` | enum: `package`, `node`, `peer` | Must equal the scope of the identifier's namespace; a scope can only refuse. |
| [`provider`](#field-provider) | `yes` | ref: `#/$defs/provider` |  |
| [`contract`](#field-contract) | `yes` | ref: `package-capability-contract.v1.schema.json#/$defs/member` | The `package-capability-contract.v1` member; its digest is the `contract/digest` grants and requirement edges bind. |
| [`component-contract`](#field-component-contract) | `yes` | ref: `package-capability-contract.v1.schema.json#/$defs/member` | The provider's `middleware-component-contract.v1` member, whose `provides[]` carries exactly this identifier and contract digest and whose `effects` declare every referenced effect. |
| [`effect/refs`](#field-effect-refs) | `yes` | array | Effect ids of the component contract an invocation may produce. Their most restrictive class is the invocation's recovery class; an empty list declares a read-only operation. |
| [`budget`](#field-budget) | `yes` | object |  |
| [`replay/window-ms`](#field-replay-window-ms) | `yes` | integer | Replay window, at most the node's ceiling; `protected-until` is fixed from it at admission. |
| [`requires/capabilities`](#field-requires-capabilities) | `yes` | array | Registered base capabilities the implementation reaches the host through. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`provider`](#def-provider) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `package-capability-declaration.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: string

`name@scope-ns:did:key:z…/package`, read by the one capability identifier grammar.

<a id="field-capability-scope"></a>
## `capability/scope`

- Required: `yes`
- Shape: enum: `package`, `node`, `peer`

Must equal the scope of the identifier's namespace; a scope can only refuse.

<a id="field-provider"></a>
## `provider`

- Required: `yes`
- Shape: ref: `#/$defs/provider`

<a id="field-contract"></a>
## `contract`

- Required: `yes`
- Shape: ref: `package-capability-contract.v1.schema.json#/$defs/member`

The `package-capability-contract.v1` member; its digest is the `contract/digest` grants and requirement edges bind.

<a id="field-component-contract"></a>
## `component-contract`

- Required: `yes`
- Shape: ref: `package-capability-contract.v1.schema.json#/$defs/member`

The provider's `middleware-component-contract.v1` member, whose `provides[]` carries exactly this identifier and contract digest and whose `effects` declare every referenced effect.

<a id="field-effect-refs"></a>
## `effect/refs`

- Required: `yes`
- Shape: array

Effect ids of the component contract an invocation may produce. Their most restrictive class is the invocation's recovery class; an empty list declares a read-only operation.

<a id="field-budget"></a>
## `budget`

- Required: `yes`
- Shape: object

<a id="field-replay-window-ms"></a>
## `replay/window-ms`

- Required: `yes`
- Shape: integer

Replay window, at most the node's ceiling; `protected-until` is fixed from it at admission.

<a id="field-requires-capabilities"></a>
## `requires/capabilities`

- Required: `yes`
- Shape: array

Registered base capabilities the implementation reaches the host through.

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-provider"></a>
## `$defs.provider`

- Shape: object
