# Node Succession v1

Source schema: [`doc/schemas/node-succession.v1.schema.json`](../../schemas/node-succession.v1.schema.json)

Local proof that one node identity key explicitly names a successor node identity key. The proof is a signed fact, not an automatic transfer of endpoint evidence, TLS pins, routing trust, or operator acceptance.

## Governing Basis

- [`doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`](../../project/40-proposals/014-node-transport-and-discovery-mvp.md)
- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/60-solutions/000-node/000-node.md`](../../project/60-solutions/000-node/000-node.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `node-succession.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`succession/id`](#field-succession-id) | `yes` | string | Digest-derived identifier of the signed payload. |
| [`old/node-id`](#field-old-node-id) | `yes` | string |  |
| [`old/key-public`](#field-old-key-public) | `yes` | string |  |
| [`new/node-id`](#field-new-node-id) | `yes` | string |  |
| [`new/key-public`](#field-new-key-public) | `yes` | string |  |
| [`succession/mode`](#field-succession-mode) | `yes` | enum: `planned-rotation`, `emergency-rotation`, `operator-rekey` |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`reason/ref`](#field-reason-ref) | `no` | string |  |
| [`revocation/ref`](#field-revocation-ref) | `no` | string |  |
| [`proof/old`](#field-proof-old) | `yes` | ref: `#/$defs/proof` |  |
| [`proof/new`](#field-proof-new) | `yes` | ref: `#/$defs/proof` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`proof`](#def-proof) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `node-succession.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-succession-id"></a>
## `succession/id`

- Required: `yes`
- Shape: string

Digest-derived identifier of the signed payload.

<a id="field-old-node-id"></a>
## `old/node-id`

- Required: `yes`
- Shape: string

<a id="field-old-key-public"></a>
## `old/key-public`

- Required: `yes`
- Shape: string

<a id="field-new-node-id"></a>
## `new/node-id`

- Required: `yes`
- Shape: string

<a id="field-new-key-public"></a>
## `new/key-public`

- Required: `yes`
- Shape: string

<a id="field-succession-mode"></a>
## `succession/mode`

- Required: `yes`
- Shape: enum: `planned-rotation`, `emergency-rotation`, `operator-rekey`

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

<a id="field-reason-ref"></a>
## `reason/ref`

- Required: `no`
- Shape: string

<a id="field-revocation-ref"></a>
## `revocation/ref`

- Required: `no`
- Shape: string

<a id="field-proof-old"></a>
## `proof/old`

- Required: `yes`
- Shape: ref: `#/$defs/proof`

<a id="field-proof-new"></a>
## `proof/new`

- Required: `yes`
- Shape: ref: `#/$defs/proof`

## Definition Semantics

<a id="def-proof"></a>
## `$defs.proof`

- Shape: object
