# Nym Renew Rejected v1

Source schema: [`doc/schemas/nym-renew-rejected.v1.schema.json`](../../schemas/nym-renew-rejected.v1.schema.json)

Machine-readable schema for a coarse council-issued rejection of a nym renewal request. The rejection is intentionally low-detail so that non-renewal does not disclose the hidden participant-level cause.

## Governing Basis

- [`doc/project/20-memos/nym-layer-roadmap-and-revocable-anonymity.md`](../../project/20-memos/nym-layer-roadmap-and-revocable-anonymity.md)
- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`rejection/id`](#field-rejection-id) | `yes` | string | Stable identifier of this rejection artifact. |
| [`request/id`](#field-request-id) | `yes` | string | Identifier of the rejected renewal request. |
| [`request/type`](#field-request-type) | `yes` | const: `nym/renew-rejected` | Application-level response discriminator. |
| [`nym/id`](#field-nym-id) | `yes` | string | Nym line whose renewal was rejected. |
| [`issuer/id`](#field-issuer-id) | `yes` | string | Issuing council identity in canonical `council:did:key:z...` form. |
| [`created-at`](#field-created-at) | `yes` | string | Creation timestamp of the rejection artifact. |
| [`reason/class`](#field-reason-class) | `yes` | string | Coarse rejection class. Implementations should prefer opaque values such as `policy` rather than disclosing hidden participant-level causes. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-rejection-id"></a>
## `rejection/id`

- Required: `yes`
- Shape: string

Stable identifier of this rejection artifact.

<a id="field-request-id"></a>
## `request/id`

- Required: `yes`
- Shape: string

Identifier of the rejected renewal request.

<a id="field-request-type"></a>
## `request/type`

- Required: `yes`
- Shape: const: `nym/renew-rejected`

Application-level response discriminator.

<a id="field-nym-id"></a>
## `nym/id`

- Required: `yes`
- Shape: string

Nym line whose renewal was rejected.

<a id="field-issuer-id"></a>
## `issuer/id`

- Required: `yes`
- Shape: string

Issuing council identity in canonical `council:did:key:z...` form.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Creation timestamp of the rejection artifact.

<a id="field-reason-class"></a>
## `reason/class`

- Required: `yes`
- Shape: string

Coarse rejection class. Implementations should prefer opaque values such as `policy` rather than disclosing hidden participant-level causes.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
