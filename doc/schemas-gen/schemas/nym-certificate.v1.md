# Nym Certificate v1

Source schema: [`doc/schemas/nym-certificate.v1.schema.json`](../../schemas/nym-certificate.v1.schema.json)

Machine-readable schema for a council-issued application-layer pseudonym certificate. This artifact remains above the transport boundary and can be attached to nym-authored application messages.

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
| [`nym/id`](#field-nym-id) | `yes` | string | Certified nym identity. |
| [`epoch`](#field-epoch) | `yes` | integer | Epoch number of this pseudonym line. |
| [`issued-at`](#field-issued-at) | `yes` | string | Issue timestamp of the certificate. |
| [`expires-at`](#field-expires-at) | `yes` | string | End of ordinary validity for application-message signing. |
| [`leniency-until`](#field-leniency-until) | `yes` | string | End of grace semantics for continuity work. After this moment the old line is dead. |
| [`issuer/id`](#field-issuer-id) | `yes` | string | Issuing council identity in canonical `council:did:key:z...` form. |
| [`line/predecessor-nym-id`](#field-line-predecessor-nym-id) | `no` | string | Optional public predecessor line when the nym continues an earlier visible pseudonymous history. |
| [`line/succession`](#field-line-succession) | `no` | ref: `nym-succession.v1.schema.json` | Optional public continuity proof signed by the predecessor nym. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "line/predecessor-nym-id"
  ]
}
```

Then:

```json
{
  "required": [
    "line/succession"
  ]
}
```

### Rule 2

When:

```json
{
  "required": [
    "line/succession"
  ]
}
```

Then:

```json
{
  "required": [
    "line/predecessor-nym-id"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-nym-id"></a>
## `nym/id`

- Required: `yes`
- Shape: string

Certified nym identity.

<a id="field-epoch"></a>
## `epoch`

- Required: `yes`
- Shape: integer

Epoch number of this pseudonym line.

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

Issue timestamp of the certificate.

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

End of ordinary validity for application-message signing.

<a id="field-leniency-until"></a>
## `leniency-until`

- Required: `yes`
- Shape: string

End of grace semantics for continuity work. After this moment the old line is dead.

<a id="field-issuer-id"></a>
## `issuer/id`

- Required: `yes`
- Shape: string

Issuing council identity in canonical `council:did:key:z...` form.

<a id="field-line-predecessor-nym-id"></a>
## `line/predecessor-nym-id`

- Required: `no`
- Shape: string

Optional public predecessor line when the nym continues an earlier visible pseudonymous history.

<a id="field-line-succession"></a>
## `line/succession`

- Required: `no`
- Shape: ref: `nym-succession.v1.schema.json`

Optional public continuity proof signed by the predecessor nym.

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
