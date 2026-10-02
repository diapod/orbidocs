# Package Capability Contract v1

Source schema: [`doc/schemas/package-capability-contract.v1.schema.json`](../../schemas/package-capability-contract.v1.schema.json)

The input and output contract of one package capability (P093 §6). It names its schemas as immutable package members by path and digest; the host keeps the members it verified at import and conformance and compiles the schemas offline at activation. `contract/digest` is `sha256:` over the base64url-no-pad JCS v1 bytes of this document. A schema `$ref` resolves only within its document, to a member listed in `refs`, or to a canonical Node schema id; nothing is fetched.

## Governing Basis

- [`doc/project/40-proposals/093-package-scoped-private-capabilities.md`](../../project/40-proposals/093-package-scoped-private-capabilities.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `package-capability-contract.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`schema/dialect`](#field-schema-dialect) | `yes` | const: `https://json-schema.org/draft/2020-12/schema` |  |
| [`input/schema`](#field-input-schema) | `yes` | ref: `#/$defs/member` | The schema every invocation input must satisfy before the admission point. |
| [`output/schema`](#field-output-schema) | `yes` | ref: `#/$defs/member` | The schema every provider output must satisfy before it is recorded completed or released. |
| [`refs`](#field-refs) | `no` | object | Further package members the two schemas may `$ref`, by path and digest. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`path`](#def-path) | string | A relative package member path: lowercase segments that never start with `.`, so `..` and absolute paths are unrepresentable. |
| [`digest`](#def-digest) | string | `sha256:` over the base64url-no-pad JCS v1 bytes of the member document. |
| [`member`](#def-member) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `package-capability-contract.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-schema-dialect"></a>
## `schema/dialect`

- Required: `yes`
- Shape: const: `https://json-schema.org/draft/2020-12/schema`

<a id="field-input-schema"></a>
## `input/schema`

- Required: `yes`
- Shape: ref: `#/$defs/member`

The schema every invocation input must satisfy before the admission point.

<a id="field-output-schema"></a>
## `output/schema`

- Required: `yes`
- Shape: ref: `#/$defs/member`

The schema every provider output must satisfy before it is recorded completed or released.

<a id="field-refs"></a>
## `refs`

- Required: `no`
- Shape: object

Further package members the two schemas may `$ref`, by path and digest.

## Definition Semantics

<a id="def-path"></a>
## `$defs.path`

- Shape: string

A relative package member path: lowercase segments that never start with `.`, so `..` and absolute paths are unrepresentable.

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

`sha256:` over the base64url-no-pad JCS v1 bytes of the member document.

<a id="def-member"></a>
## `$defs.member`

- Shape: object
