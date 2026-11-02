# Nym Renew Request v1

Source schema: [`doc/schemas/nym-renew-request.v1.schema.json`](../../schemas/nym-renew-request.v1.schema.json)

Participant-signed renewal request. Predecessor control is not a succession and does not bind the not-yet-issued successor certificate.

## Governing Basis

- [`doc/project/20-memos/nym-layer-roadmap-and-revocable-anonymity.md`](../../project/20-memos/nym-layer-roadmap-and-revocable-anonymity.md)
- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`request/id`](#field-request-id) | `yes` | string | Stable identifier of this renewal request. |
| [`request/type`](#field-request-type) | `yes` | const: `nym/renew` | Application-level request discriminator. |
| [`participant/id`](#field-participant-id) | `yes` | string | Participant identity asking for renewal. |
| [`created-at`](#field-created-at) | `yes` | string | Creation timestamp of the renewal request. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |
| [`predecessor/certificate`](#field-predecessor-certificate) | `yes` | string |  |
| [`successor/nym`](#field-successor-nym) | `yes` | string |  |
| [`issuer/id`](#field-issuer-id) | `yes` | string |  |
| [`not-after`](#field-not-after) | `yes` | string |  |
| [`predecessor/control-proof`](#field-predecessor-control-proof) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |

## Conditional Rules

### Rule 1

Constraint:

```json
{
  "not": {
    "required": [
      "succession"
    ]
  }
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-request-id"></a>
## `request/id`

- Required: `yes`
- Shape: string

Stable identifier of this renewal request.

<a id="field-request-type"></a>
## `request/type`

- Required: `yes`
- Shape: const: `nym/renew`

Application-level request discriminator.

<a id="field-participant-id"></a>
## `participant/id`

- Required: `yes`
- Shape: string

Participant identity asking for renewal.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Creation timestamp of the renewal request.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

<a id="field-predecessor-certificate"></a>
## `predecessor/certificate`

- Required: `yes`
- Shape: string

<a id="field-successor-nym"></a>
## `successor/nym`

- Required: `yes`
- Shape: string

<a id="field-issuer-id"></a>
## `issuer/id`

- Required: `yes`
- Shape: string

<a id="field-not-after"></a>
## `not-after`

- Required: `yes`
- Shape: string

<a id="field-predecessor-control-proof"></a>
## `predecessor/control-proof`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
