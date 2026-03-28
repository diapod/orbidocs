# Nym Renew Request v1

Source schema: [`doc/schemas/nym-renew-request.v1.schema.json`](../../schemas/nym-renew-request.v1.schema.json)

Machine-readable schema for a participant-signed renewal request carrying public nym continuity proof for the next epoch.

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
| [`request/id`](#field-request-id) | `yes` | string | Stable identifier of this renewal request. |
| [`request/type`](#field-request-type) | `yes` | const: `nym/renew` | Application-level request discriminator. |
| [`participant/id`](#field-participant-id) | `yes` | string | Participant identity asking for renewal. |
| [`succession`](#field-succession) | `yes` | ref: `nym-succession.v1.schema.json` | Public continuity proof already signed by the old nym. |
| [`created-at`](#field-created-at) | `yes` | string | Creation timestamp of the renewal request. |
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

<a id="field-succession"></a>
## `succession`

- Required: `yes`
- Shape: ref: `nym-succession.v1.schema.json`

Public continuity proof already signed by the old nym.

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

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
