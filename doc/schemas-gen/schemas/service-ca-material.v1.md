# Service CA Material v1

Source schema: [`doc/schemas/service-ca-material.v1.schema.json`](../../schemas/service-ca-material.v1.schema.json)

Signed governance-published trust material candidate for a scoped service CA. This artifact is not a local trust decision; a node may use it only after local policy accepts the issuer, scope, and policy reference.

## Governing Basis

- [`doc/project/40-proposals/056-orbiplex-tls-trust-policy.md`](../../project/40-proposals/056-orbiplex-tls-trust-policy.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `service-ca-material.v1` | Schema discriminator. MUST be exactly `service-ca-material.v1`. |
| [`ca/id`](#field-ca-id) | `yes` | string | Stable identifier of this CA material artifact or CA lineage member. |
| [`service/kind`](#field-service-kind) | `yes` | enum: `seed-directory`, `agora`, `artifact-delivery`, `inac`, `other` | Service surface for which this CA material is being announced. |
| [`scope`](#field-scope) | `yes` | ref: `#/$defs/scope` |  |
| [`material`](#field-material) | `yes` | ref: `#/$defs/material` |  |
| [`valid/from`](#field-valid-from) | `yes` | string | Start of the publication validity window. |
| [`valid/until`](#field-valid-until) | `yes` | string | End of the publication validity window. Nodes MUST ignore this candidate after this time unless a newer accepted artifact supersedes it. |
| [`rotation`](#field-rotation) | `no` | ref: `#/$defs/rotation` |  |
| [`issuer`](#field-issuer) | `yes` | ref: `#/$defs/issuer` |  |
| [`policy/ref`](#field-policy-ref) | `no` | string | Optional local-policy reference or governance policy identifier that tells a node which acceptance rule may authorize this trust material. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`scope`](#def-scope) | object | Scope in which this CA material may be considered. Local trust policy MUST match against this scope before using the material. |
| [`material`](#def-material) | object |  |
| [`rotation`](#def-rotation) | object |  |
| [`issuer`](#def-issuer) | object |  |
| [`signature`](#def-signature) | object |  |
| [`sha256Digest`](#def-sha256digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `service-ca-material.v1`

Schema discriminator. MUST be exactly `service-ca-material.v1`.

<a id="field-ca-id"></a>
## `ca/id`

- Required: `yes`
- Shape: string

Stable identifier of this CA material artifact or CA lineage member.

<a id="field-service-kind"></a>
## `service/kind`

- Required: `yes`
- Shape: enum: `seed-directory`, `agora`, `artifact-delivery`, `inac`, `other`

Service surface for which this CA material is being announced.

<a id="field-scope"></a>
## `scope`

- Required: `yes`
- Shape: ref: `#/$defs/scope`

<a id="field-material"></a>
## `material`

- Required: `yes`
- Shape: ref: `#/$defs/material`

<a id="field-valid-from"></a>
## `valid/from`

- Required: `yes`
- Shape: string

Start of the publication validity window.

<a id="field-valid-until"></a>
## `valid/until`

- Required: `yes`
- Shape: string

End of the publication validity window. Nodes MUST ignore this candidate after this time unless a newer accepted artifact supersedes it.

<a id="field-rotation"></a>
## `rotation`

- Required: `no`
- Shape: ref: `#/$defs/rotation`

<a id="field-issuer"></a>
## `issuer`

- Required: `yes`
- Shape: ref: `#/$defs/issuer`

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `no`
- Shape: string

Optional local-policy reference or governance policy identifier that tells a node which acceptance rule may authorize this trust material.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

## Definition Semantics

<a id="def-scope"></a>
## `$defs.scope`

- Shape: object

Scope in which this CA material may be considered. Local trust policy MUST match against this scope before using the material.

<a id="def-material"></a>
## `$defs.material`

- Shape: object

<a id="def-rotation"></a>
## `$defs.rotation`

- Shape: object

<a id="def-issuer"></a>
## `$defs.issuer`

- Shape: object

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object

<a id="def-sha256digest"></a>
## `$defs.sha256Digest`

- Shape: string
