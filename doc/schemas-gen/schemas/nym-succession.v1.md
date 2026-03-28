# Nym Succession v1

Source schema: [`doc/schemas/nym-succession.v1.schema.json`](../../schemas/nym-succession.v1.schema.json)

Machine-readable schema for a public continuity proof from an old pseudonym line to the next nym epoch.

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
| [`old-nym/id`](#field-old-nym-id) | `yes` | string | Public predecessor nym line. |
| [`new-nym/id`](#field-new-nym-id) | `yes` | string | Public successor nym line. |
| [`epoch`](#field-epoch) | `yes` | integer | New epoch number claimed by the succession proof. |
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

<a id="field-old-nym-id"></a>
## `old-nym/id`

- Required: `yes`
- Shape: string

Public predecessor nym line.

<a id="field-new-nym-id"></a>
## `new-nym/id`

- Required: `yes`
- Shape: string

Public successor nym line.

<a id="field-epoch"></a>
## `epoch`

- Required: `yes`
- Shape: integer

New epoch number claimed by the succession proof.

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
